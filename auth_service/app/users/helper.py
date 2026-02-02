from app.users.schemas import SUserJWT
from app.users.utils import encode_token


def create_JWT(
    token_data: dict,
    token_type: str,
    expire_minutes,
) -> str:
    payload_jwt = {"type": token_type}
    payload_jwt.update(token_data)
    return encode_token(payload_jwt, time=expire_minutes)


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

