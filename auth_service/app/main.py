from collections.abc import AsyncIterator
from contextlib import asynccontextmanager


from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from prometheus_fastapi_instrumentator import Instrumentator
from sqladmin import Admin

from app.users.router import router as router_users
from app.users.JWT_session.router import router as router_JWT
from app.core.redis import redis_manager
from app.database import engin
from app.admin.auth import authentication_backend
from app.admin.views import SessionAdmin, UserAdmin


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"]
)


@asynccontextmanager
async def lifespan(app_instance: FastAPI) -> AsyncIterator[None]:
    redis_client = redis_manager.get_client()
    FastAPICache.init(RedisBackend(redis_client), prefix="cache")
    
    instrumentator.expose(app_instance)

    yield

    await redis_manager.close()


app = FastAPI(
    lifespan=lifespan,
    title="Auth Service",
    root_path="/auth" 
)


app.include_router(router_users)
app.include_router(router_JWT)


@cache()
async def get_cache():
    return 1


instrumentator.instrument(app).expose(app, endpoint="/metrics", include_in_schema=True)

admin = Admin(app, engin, authentication_backend=authentication_backend, base_url="/admin")

admin.add_view(UserAdmin)
admin.add_view(SessionAdmin)

