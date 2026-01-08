from datetime import datetime
from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError

from app.config import setting
from app.users.models import Users
from app.users.service import UsersService

def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_curret_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, setting.SALT, setting.ALGORITHN
        )   
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await UsersService.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    

    return user


async def get_curret_admin_user(current_user: Users = Depends(get_curret_user)):
    # if current_user.role != "admin":
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return current_user