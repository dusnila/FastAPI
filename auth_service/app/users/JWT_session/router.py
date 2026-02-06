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
async def get_all_sessions(user: User = Depends(get_curret_user)):
    """Позволяет пользователю увидеть, где выполнен вход"""
    return await SessionService.find_all(user_id=user.id)


@router.get("/sessions/current", summary="Данные текущей сессии")
async def get_current_session_info(refresh_token: str = Depends(get_refresh_token)):
    """Информация о конкретном текущем соединении"""
    return await SessionService.find_all(refresh_JWT=refresh_token)

@router.delete("/sessions/other", summary="Выйти на всех других устройствах")
async def delete_all_other_sessions(RefreshToken: str = Depends(get_refresh_token), user: User = Depends(get_curret_user)):
    """Удаляет все сессии пользователя, кроме той, с которой сделан запрос"""
    return await SessionService.logout_others(user_id=user.id, refresh_token= RefreshToken)

@router.delete("/sessions/delete", summary="Завершить конкретную сессию")
async def delete_session_by_token(RefreshToken: str = Depends(get_refresh_token)):
    """Удаление сессии (например, если телефон украден)"""
    return await SessionService.delete(refresh_JWT=RefreshToken)


