from datetime import datetime, timedelta
from fastapi import Request
from passlib.context import CryptContext
from jose import JWTError, jwt
import bcrypt

from app.config import setting
from app.exceptions import IncorrectTokenFormatException, TokenAccessAbsenException, TokenRefreshAbsenException, TokenExpiredException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def encode_token(data: dict, time: int) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=time)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, setting.PRIVATE_KEY, setting.ALGORITHM
    )
    return encoded_jwt


def  decode_access_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAccessAbsenException

    try:
        payload = jwt.decode(
            token, setting.PUBLIC_KEY, setting.ALGORITHM
        )   
    except JWTError:
        raise IncorrectTokenFormatException
    
    expire = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now().timestamp()):
        raise TokenExpiredException
    
    return payload


def decode_refresh_token(request: Request):
    token = request.cookies.get("booking_refresh_token")
    if not token:
        raise TokenRefreshAbsenException
    
    try:
        payload = jwt.decode(
            token, setting.PUBLIC_KEY, setting.ALGORITHM
        )   
    except JWTError:
        raise IncorrectTokenFormatException
    
    expire = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now().timestamp()):
        raise TokenExpiredException
    
    return payload