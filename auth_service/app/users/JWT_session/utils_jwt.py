from datetime import datetime, timedelta, timezone
from fastapi import Request
from jose import JWTError, jwt, ExpiredSignatureError

from app.config import setting
from app.exceptions import IncorrectTokenFormatException, TokenAbsenException, TokenExpiredException
from app.users.JWT_session.schemas import SUserJWT


def create_access_token(user: SUserJWT) -> str:
    payload_jwt = {
        "sub": user.username,
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
    expire = datetime.now(timezone.utc) + timedelta(minutes=time)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, setting.PRIVATE_KEY, setting.ALGORITHM
    )
    return encoded_jwt


def  decode_access_token(request: Request):
    token = get_token(request, "booking_access_token")

    return decode_token(token, "access")


def decode_refresh_token(request: Request):
    token = get_token(request, "booking_refresh_token")

    return decode_token(token, "refresh")


def decode_token(token: str, expected_type: str):
    try:
        payload = jwt.decode(token, setting.PUBLIC_KEY, setting.ALGORITHM)
        
        if payload.get("type") != expected_type:
            raise IncorrectTokenFormatException
            
        return payload
    except ExpiredSignatureError:
        raise TokenExpiredException   
    except JWTError:
        raise IncorrectTokenFormatException


def get_refresh_token(request: Request):
    return get_token(request, "booking_refresh_token")


def get_token(request: Request, name_token: str):
    token = request.cookies.get(name_token)
    if not token:
        raise TokenAbsenException
    return token
    
