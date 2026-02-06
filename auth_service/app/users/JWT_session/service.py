from datetime import datetime, timedelta, timezone

from fastapi import Response
from sqlalchemy import and_, delete, insert, update

from app.config import setting
from app.database import async_session_maker
from app.service.base import BaseService
from app.users.models import User
from app.users.schemas import SUser

from app.users.JWT_session.models import Session
from app.users.JWT_session.schemas import SUserJWT, SSession
from app.users.JWT_session.utils_jwt import create_refresh_token, create_access_token

from app.exceptions import TokenNotFoundException


class SessionService(BaseService):
    model = Session


    @classmethod
    async def add_session(cls, session_data: SSession) -> None:
        """Добавление новой сессии при логине"""
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        expire_delta = timedelta(minutes=setting.TIME_LIVE_REFRESH_TOKEN)

        async with async_session_maker() as session:
            query = insert(cls.model).values(
                **session_data.model_dump(),
                created_at=now,
                expires_at=now + expire_delta
            )
            await session.execute(query)
            await session.commit()


    @classmethod
    async def update_session(cls, old_token: str, user: User) -> str:
        """
        Обновляет существующую сессию: генерирует новый токен и продлевает время жизни.
        Возвращает новый refresh_token.
        """
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        new_expire = now + timedelta(minutes=setting.TIME_LIVE_REFRESH_TOKEN)
        
        user_schema = SUser.model_validate(user)
        new_token = create_refresh_token(user_schema)

        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.refresh_JWT == old_token)
                .values(
                    refresh_JWT=new_token,
                    created_at=now,
                    expires_at=new_expire
                )
                .returning(cls.model.refresh_JWT)
            )

            result = await session.execute(query)
            updated_token = result.scalar_one_or_none()
            
            if not updated_token:
                await session.rollback()
                raise TokenNotFoundException 

            await session.commit()
            return updated_token


    @classmethod
    async def refresh_tokens(
        cls,
        response: Response,
        old_refresh_token: str,
        user: User
    ) -> dict:
        """Комплексный метод: обновление в БД + установка новых кук"""
        
        new_refresh_token = await cls.update_session(
            old_token=old_refresh_token, 
            user=user
        )

        user_jwt_schema = SUserJWT.model_validate(user)
        new_access_token = create_access_token(user=user_jwt_schema)

        # Access Token
        response.set_cookie(
            "booking_access_token", 
            new_access_token, 
            httponly=True,
            # secure=True,
            samesite="lax"
        )
        
        # Refresh Token
        response.set_cookie(
            "booking_refresh_token", 
            new_refresh_token, 
            httponly=True,
            # secure=True,
            samesite="lax"
        )

        return {"detail": "Токены успешно обновлены"}


    @classmethod
    async def logout_others(cls, user_id: int, current_token: str) -> int:
        """
        Удаляет все сессии пользователя, кроме текущей.
        Возвращает количество удаленных записей.
        """
        async with async_session_maker() as session:
            query = delete(cls.model).where(
                and_(
                    cls.model.user_id == user_id,
                    cls.model.refresh_JWT != current_token
                )
            )
            
            result = await session.execute(query)
            await session.commit()
            return result.rowcount