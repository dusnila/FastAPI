from fastapi import Depends, Request, Response

from app.exceptions import  IncorrectTokenFormatException, TokenAbsenException, TokenExpiredException, UserIsNotException, UserIsNotUnathorized
from app.users.models import User
from app.users.service import UsersService
from app.users.JWT_session.utils_jwt import decode_access_token, decode_refresh_token, get_token
from app.users.JWT_session.service import SessionService


async def get_curret_user(request: Request, response: Response):
    try:
        payload = decode_access_token(request)
        username = payload.get("sub")

    except TokenExpiredException:
        try:
            refreshTokenPayload = decode_refresh_token(request)
            username = refreshTokenPayload.get("sub")

            user = await UsersService.find_one_or_none(username=username)
            if not user:
                raise UserIsNotException
            
            old_refresh_token = get_token(request, "booking_refresh_token")

            await SessionService.refresh_tokens(response, old_refresh_token, user)

            return user
        
        except (TokenExpiredException, TokenAbsenException, IncorrectTokenFormatException):
            raise TokenAbsenException

    if not username:
        raise UserIsNotException
    
    user = await UsersService.find_one_or_none(username=username)
    if not user:
        raise UserIsNotException
    
    return user



async def get_curret_admin_user(current_user: User = Depends(get_curret_user)):
    if current_user.role != "admin":
        raise UserIsNotUnathorized
    return current_user