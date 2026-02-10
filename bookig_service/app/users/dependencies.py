from fastapi import Request
from jose import ExpiredSignatureError, JWTError, jwt

from app.exceptions import  IncorrectTokenFormatException, IncorrectTypeTokenException, TokenAbsenException, TokenExpiredException, UserIDNotFaundExeption, UserIsNotException
from app.config import setting
from app.users.schemas import SUser


async def get_curret_user(request: Request):
        token = request.cookies.get("booking_access_token")
        if not token:
            raise TokenAbsenException
        try:
            payload = jwt.decode(
                token,
                setting.PUBLIC_KEY,
                setting.ALGORITHM
            )

            if payload.get("type") != "access":
                raise IncorrectTypeTokenException

            user_id = payload.get("sub")
            if user_id is None:
                raise UserIDNotFaundExeption

            return SUser(
                 id= int(user_id),
                 username=payload.get("username"),
                 email=payload.get("email"),
                 role=payload.get("role")
            )


        except ExpiredSignatureError:
            raise TokenExpiredException
        
        except JWTError:
            raise IncorrectTokenFormatException