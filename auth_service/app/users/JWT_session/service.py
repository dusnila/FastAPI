from datetime import datetime, timedelta, timezone

from fastapi import Response
from sqlalchemy import insert, update
from app.users.JWT_session.models import Session
from app.service.base import BaseService
from app.users.JWT_session.schemas import SUserJWT, SSession
from app.config import setting
from app.database import async_session_maker
from app.users.JWT_session.utils_jwt import create_refresh_token
from app.users.models import User
from app.exceptions import TokenNotFoundException
from app.users.schemas import SUser


class SessionService(BaseService):
    model = Session

    @classmethod
    async def add_session(cls, session_data: SSession):
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        expire = now + timedelta(minutes=setting.TIME_LIVE_REFRESH_TOKEN)

        async with async_session_maker() as session:
            query = insert(cls.model).values(
                **session_data.model_dump(),
                created_at = now,
                expires_at = expire
            )

            await session.execute(query)
            await session.commit()

    
    @classmethod
    async def update_session(cls, refresh_token: str, user: User):
        user_shema = SUser.model_validate(user)

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        new_expires_at = now + timedelta(minutes=setting.TIME_LIVE_REFRESH_TOKEN)
        new_refresh_JWT = create_refresh_token(user_shema)

        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.refresh_JWT == refresh_token)
                .values(
                    created_at = now,
                    expires_at = new_expires_at,
                    refresh_JWT = new_refresh_JWT
                )
                .returning(cls.model.refresh_JWT)
            )

            result = await session.execute(query)
            updated_token = result.scalar_one_or_none()
            await session.commit()

            if not updated_token:
                raise TokenNotFoundException 

            return updated_token
        

    @classmethod
    async def refresh_tokens(cls, response: Response, old_refresh_token: str, user: User):

        new_refresh_token = await SessionService.update_session(
        refresh_token=old_refresh_token, 
        user=user
        )

    # new_access_token = create_access_token(user=SUserJWT.model_validate(user))
    # response.set_cookie("booking_access_token", new_access_token, httponly=True)

        response.set_cookie(
            "booking_refresh_token", 
            new_refresh_token, 
            httponly=True,
            # secure=True,
            # samesite="lax"
        )

        return {"detail": "Токены успешно обновлены"}