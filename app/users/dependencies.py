from datetime import datetime
from fastapi import Depends, Request
from jose import jwt, JWTError

from app.config import setting
from app.exceptions import IncorrectTokenFormatException, TokenAbsenException, TokenExpiredException, UserIsNotException
from app.users.models import Users
from app.users.service import UsersService

def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsenException
    return token


async def get_curret_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, setting.SALT, setting.ALGORITHN
        )   
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotException
    user = await UsersService.find_by_id(int(user_id))
    if not user:
        raise UserIsNotException
    

    return user


async def get_curret_admin_user(current_user: Users = Depends(get_curret_user)):
    return current_user