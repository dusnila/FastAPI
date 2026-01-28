from fastapi import APIRouter, Depends, Response, status
from pydantic import EmailStr

from app.users.dependencies import get_curret_admin_user, get_curret_user
from app.users.models import Users
from app.users.service import UsersService
from app.users.schemas import SSendMessageEmail, SUserAuth, SUserRegister

router = APIRouter(
    tags=["Auth"],
)

@router.post(
        "/register",
        status_code=status.HTTP_201_CREATED,
        summary="Регистрация нового пользователя",
        description="Регистрирует пользователя по email, username и паролю. Проверяет уникальность данных.",
        responses={
            status.HTTP_409_CONFLICT:{
                "description": "Почта или никнейм уже существуют",
                "content": {"application/json": {"example": {"detail": "Пользователь уже существует"}}}
            },
        }
)
async def register_user(user_data: SUserRegister):
    await UsersService.register_user_service(user_data)
    return {"detail": "подтвердите почту"}


@router.get(
    "/verify",
    summary="подтверждение регистрации"
)
async def verify_email(token: str):
    responce = await UsersService.verify_email_service(token)
    return responce


@router.post(
    "/sendVerify",
    summary="повторное отпровления подверждение регистрации"
)
async def send_verify(email: SSendMessageEmail):
    responce = await UsersService.send_message_verify_service(str(email))
    return responce


@router.post(
        "/login"
)
async def login_user(response: Response, user_data: SUserAuth):
    access_token = await UsersService.login_and_get_token(response, user_data)
    return access_token


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_curret_user)):
    return current_user

@router.get("/all")
async def read_users_all(current_user: Users = Depends(get_curret_admin_user)):
    return await UsersService.find_all()