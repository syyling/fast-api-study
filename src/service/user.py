import bcrypt
from datetime import datetime, timedelta
from jose import jwt
import random, time

class UserService:
    encoding: str = "UTF-8"
    secret_key: str = "662108463a72d1c9c835bd2125ad630d53309bbe357a545ea63fabd8a6c4e1ce"
    jwt_algorithm: str = "HS256"

    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding), bcrypt.gensalt()
        )
        return hashed_password.decode(self.encoding)

    def verify_password(
            self, plain_password: str, hashed_password: str
    ) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding),
        )

    def create_jwt(self, username: str) -> str:
        return jwt.encode(
            {
                "sub": username,
                "exp": datetime.now() + timedelta(days=1)
             },
            self.secret_key,
            self.jwt_algorithm
        )

    def decode_token(self, access_token: str) -> str:
        payload: dict =  jwt.decode(
            access_token, self.secret_key, self.jwt_algorithm
        )
        # expire check 코드도 원래 있어야 함!!
        return payload["sub"]

    @staticmethod
    def create_otp() -> int:
        return random.randint(1000, 9999)

    @staticmethod
    def send_email_to_user(email: str) -> None:
        time.sleep(5)
        print(f"Sending email to {email}!")
