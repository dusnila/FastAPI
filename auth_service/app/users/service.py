import uuid

from fastapi import Response


from app.tasks.tasks import send_verification_email
from app.exceptions import EmailAlreadyExistsException, IncorrectEmailorPasswordException, InvalidLinkException, NotSuchUserExeption, UserNotToVerifyExeption, UsernameAlreadyExistsException
from app.users.utils import get_password_hash, verify_password, encode_access_token
from app.users.schemas import SUserAuth, SUserRegister
from app.service.base import BaseService
from app.users.models import Users
from app.core.redis import redis_manager


class UsersService(BaseService):
    model = Users

    @classmethod
    async def register_user_service(cls, user_data: SUserRegister):

        existing_user = await cls.find_one_or_none(email=user_data.email)
        if existing_user:
            raise EmailAlreadyExistsException

        existing_user = await cls.find_one_or_none(username=user_data.username)
        if existing_user:
            raise UsernameAlreadyExistsException

        hashed_password = get_password_hash(user_data.password)

        await cls.add(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )

        await cls.send_message_verify_service(user_data.email)


    @classmethod
    async def verify_email_service(cls, token: str):
        email = await redis_manager.get_email(token)
        if not email:
            raise InvalidLinkException

        user = await cls.find_one_or_none(email=email)
        if not user:
            raise NotSuchUserExeption

        if user.is_active :
            return {"detail": "Почта уже была подтверждена ранее"}
        
        await cls.update({"email": email}, is_active=True)

        await redis_manager.delete("verification", token)
        return {"detail": "Почта успешна подверждена"}


    @classmethod
    async def send_message_verify_service(cls, email: str):
        if not await cls.find_one_or_none(email=email):
            raise NotSuchUserExeption

        verification_token = str(uuid.uuid4())

        await redis_manager.set_verification_token(verification_token, email)

        send_verification_email.delay(email, verification_token)

        return {"detail": "подверждение отправлено"}

    @classmethod
    async def login_and_get_token(cls, response: Response, user_data: SUserAuth):
        user = await cls.find_one_or_none(email=user_data.email)
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise IncorrectEmailorPasswordException
        if not user.is_active:
            raise UserNotToVerifyExeption
        access_token = encode_access_token({"sub": str(user.id)})
        response.set_cookie("booking_access_token", access_token, httponly=True)
        return {"detail": "упешная авторизация"} 