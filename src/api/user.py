from fastapi import APIRouter, Depends

from database.repository import UserRepository
from schema.request import SignUpRequest
from schema.response import UserSchema
from service.user import UserService
from database.orm import User

router = APIRouter(prefix="/users")



@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
        request: SignUpRequest,
        user_service: UserService = Depends(),
        user_repository : UserRepository = Depends()
):
    # 1. request body

    # 2. password hashing
    hashed_password : str = user_service.hash_password(
        plain_password=request.password
    )

    # 3. User
    user: User = User.create(
        username=request.username,
        hashed_password=hashed_password,
    )

    # 4. db save
    user: User = user_repository.save_user(user)

    # 5. return user(id, username)
    return UserSchema.from_orm(user)