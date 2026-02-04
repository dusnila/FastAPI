from fastapi import APIRouter, Response, Depends

from app.users.JWT_session.service import SessionService
from app.users.JWT_session.utils_jwt import get_refresh_token
from app.users.dependencies import get_curret_user
from app.users.models import User


router = APIRouter(
    tags=["JWT"],
)


@router.post("/refresh", summary="Обновить токен доступа")
async def refresh_token(
    response: Response,
    old_refresh_token: str = Depends(get_refresh_token), 
    user: User = Depends(get_curret_user) 
):
    """Использует refresh_JWT для выдачи новой пары токенов"""
    return await SessionService.refresh_tokens(response, old_refresh_token, user)

@router.get("/sessions", summary="Список всех активных сессий")
async def get_all_sessions():
    """Позволяет пользователю увидеть, где выполнен вход"""
    pass

@router.get("/sessions/current", summary="Данные текущей сессии")
async def get_current_session_info():
    """Информация о конкретном текущем соединении"""
    pass

@router.delete("/sessions/other", summary="Выйти на всех других устройствах")
async def delete_all_other_sessions():
    """Удаляет все сессии пользователя, кроме той, с которой сделан запрос"""
    pass

@router.delete("/sessions/delete", summary="Завершить конкретную сессию")
async def delete_session_by_token(RefreshToken: str = Depends(get_refresh_token)):
    """Удаление сессии по ID (например, если телефон украден)"""
    return await SessionService.delete(refresh_JWT=RefreshToken)


