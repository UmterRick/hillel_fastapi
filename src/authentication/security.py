from datetime import timedelta, datetime, timezone
from typing import Union, Any
from jose import jwt
from passlib.context import CryptContext

from src.base_settings import base_settings

pwd_context = CryptContext(schemes=["bcrypt"])

def create_access_token(
        subject: Union[str, Any],
        expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire =  datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(
            minutes=base_settings.auth.access_token_expire_minutes
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, base_settings.auth.secret_key, algorithm=base_settings.auth.algorithm)
    return encoded_jwt


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


