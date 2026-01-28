from datetime import datetime
from fastapi import Depends, Request
from jose import jwt, JWTError

from app.config import setting
from app.exceptions import  UserIsNotException
from app.users.models import Users
from app.users.service import UsersService
from app.users.utils import decode_access_token


async def get_curret_user(payload = Depends(decode_access_token)):
    user_id = payload.get("sub")
    if not user_id:
        raise UserIsNotException
    
    
    user = await UsersService.find_by_id(int(user_id))
    if not user:
        raise UserIsNotException
    

    return user


async def get_curret_admin_user(current_user: Users = Depends(get_curret_user)):
    return current_user