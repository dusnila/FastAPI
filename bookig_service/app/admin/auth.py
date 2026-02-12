from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.exceptions import IncorrectEmailorPasswordException
from app.users.dependencies import get_curret_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        request.session.update({"token": "fake-token"}) 
        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:

        return True


authentication_backend = AdminAuth(secret_key="...")