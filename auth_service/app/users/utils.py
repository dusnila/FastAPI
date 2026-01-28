from datetime import datetime, timedelta
from fastapi import Request
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.config import setting
from app.exceptions import IncorrectTokenFormatException, TokenAbsenException, TokenExpiredException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def encode_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, setting.PRIVATE_KEY, setting.ALGORITHM
    )
    return encoded_jwt

def decode_access_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsenException

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