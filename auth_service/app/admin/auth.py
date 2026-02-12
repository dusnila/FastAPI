from fastapi import Response
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.exceptions import IncorrectEmailorPasswordException
from app.users.dependencies import get_curret_user
from app.users.JWT_session.utils_jwt import create_access_token
from app.users.service import UsersService
from app.users.schemas import SUser
from app.users.utils import verify_password


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await UsersService.find_one_or_none(email=email)
        user_schema = SUser.model_validate(user)

        if not user or not verify_password(password, user_schema.hashed_password):
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        
        if user:
            access_token = create_access_token(user)
            request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        
        # user = await get_curret_user(request, response)
        # if not user:
        #     return RedirectResponse(request.url_for("admin:login"), status_code=302)
        
        return True


authentication_backend = AdminAuth(secret_key="...")