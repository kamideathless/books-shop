import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class AuthJWT(BaseModel):
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


auth = AuthJWT()
