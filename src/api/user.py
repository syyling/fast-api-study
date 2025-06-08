from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks

from database.repository import UserRepository
from schema.request import SignUpRequest, LogInRequest, CreateOTPRequest, VerifyOTPRequest
from schema.response import UserSchema, JWTResponse
from security import get_access_token
from service.user import UserService
from database.orm import User
from cache import redis_client

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


@router.post("/log-in", status_code=201)
def user_log_in_handler(
        request: LogInRequest,
        user_repository: UserRepository = Depends(),
        user_service: UserService = Depends()
):
    # 1. request body(username, password)
    # 2. db read user
    user: User | None = user_repository.get_user_by_username(
        username=request.username
    )

    if not user :
        raise HTTPException(404, detail="User not found")

    # 3. password bcrypt.checkpw
    verified : bool = user_service.verify_password(
        plain_password=request.password,
        hashed_password=user.password
    )
    if not verified:
        raise HTTPException(401, detail="Not Authorized")

    # 4. create jwt
    access_token: str = user_service.create_jwt(user.username)

    # 5. return jwt
    return JWTResponse(access_token=access_token)


# 회원가입(username, password) / 로그인
# 이메일 알림: 회원가입 -> 이메일 인증 -> 유저 이메일 저장 -> 이메일 알림

@router.post("/email/otp")
def create_otp_handler(
        request: CreateOTPRequest,
        _: str = Depends(get_access_token),
        user_service: UserService = Depends()

):
    #1. access_token
    #2. request body(email)

    #3. otp create(random 4 digit)
    otp: int = user_service.create_otp()

    #4. redis otp(email, 1234, exp=3min)
    redis_client.set(request.email, str(otp))
    redis_client.expire(request.email, 3 * 600)

    #5. send otp to email
    return { "otp": otp }

@router.post("/email/otp/verify")
def verify_otp_handler(
        request: VerifyOTPRequest,
        background_tasks: BackgroundTasks,
        access_token: str = Depends(get_access_token),
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends()
):
    otp: str | None = redis_client.get(request.email)

    if not otp:
        raise HTTPException(400, detail="Bad otp Request")

    if request.otp != int(otp):
        raise HTTPException(400, detail="Bad requset Request")

    username: str = user_service.decode_token(access_token)
    user: User | None = user_repo.get_user_by_username(username=username)

    if not user:
        raise HTTPException(404, detail="User not found")

    # save email to user
    # send email to user
    background_tasks.add_task(
        user_service.send_email_to_user,
        email="admin@fastapi.com"
    )
    # user_service.send_email_to_user(email="admin@fastapi.com")
    return UserSchema.from_orm(user)