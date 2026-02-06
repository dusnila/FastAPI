from datetime import datetime, timedelta
from fastapi import Request
from jose import JWTError, jwt, ExpiredSignatureError

from app.config import setting
from app.exceptions import IncorrectTokenFormatException, TokenAccessAbsenException, TokenRefreshAbsenException, TokenExpiredException
from app.users.JWT_session.schemas import SUserJWT


def create_access_token(user: SUserJWT) -> str:
    payload_jwt = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    } 
    return create_JWT(
        token_data=payload_jwt, 
        token_type="access",
        expire_minutes=30
    )


def create_refresh_token(user: SUserJWT) -> str:
    payload_jwt = {
        "sub": user.username,
    }
    return create_JWT(
        token_data=payload_jwt,
        token_type="refresh",
        expire_minutes=7*24*60
    )


def create_JWT(
    token_data: dict,
    token_type: str,
    expire_minutes,
) -> str:
    payload_jwt = {"type": token_type}
    payload_jwt.update(token_data)
    return encode_token(payload_jwt, time=expire_minutes)


def encode_token(data: dict, time: int) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=time)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, setting.PRIVATE_KEY, setting.ALGORITHM
    )
    return encoded_jwt


def  decode_access_token(request: Request):
    token = get_token(request, "booking_access_token")

    try:
        payload = jwt.decode(
            token, setting.PUBLIC_KEY, setting.ALGORITHM
        )

    except ExpiredSignatureError:
        raise TokenExpiredException   

    except JWTError:
        raise IncorrectTokenFormatException
    
    expire = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now().timestamp()):
        raise TokenExpiredException
    
    return payload


def decode_refresh_token(request: Request):
    token = get_token(request, "booking_refresh_token")
    
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

def get_token(request: Request, type_token: str):
    token = request.cookies.get(type_token)
    if not token:
        raise TokenRefreshAbsenException
    return token

def get_refresh_token(request: Request):
    token = request.cookies.get("booking_refresh_token")
    if not token:
        raise TokenRefreshAbsenException
    return token
    
