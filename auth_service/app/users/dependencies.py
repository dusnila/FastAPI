from datetime import datetime
from fastapi import Depends, Request
from jose import jwt, JWTError

from app.config import setting
from app.exceptions import  UserIsNotException
from app.users.models import User
from app.users.service import UsersService
from app.users.JWT_session.utils_jwt import decode_access_token


async def get_curret_user(payload = Depends(decode_access_token)):
    user_name = payload.get("sub")
    if not user_name:
        raise UserIsNotException
    
    
    user = await UsersService.find_one_or_none(username=user_name)
    if not user:
        raise UserIsNotException
    

    return user


async def get_curret_admin_user(current_user: User = Depends(get_curret_user)):
    return current_user