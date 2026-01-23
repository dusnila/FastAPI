from collections.abc import AsyncIterator
from contextlib import asynccontextmanager


from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache


from app.users.router import router as router_users
from app.core.redis import redis_manager


@asynccontextmanager
async def lifespan(app_instance: FastAPI) -> AsyncIterator[None]:
    redis_client = redis_manager.get_client()
    FastAPICache.init(RedisBackend(redis_client), prefix="cache")

    yield

    await redis_manager.close()


app = FastAPI(
    lifespan=lifespan,
    title="Auth Service",
    root_path="/auth" 
)


app.include_router(router_users)


@cache()
async def get_cache():
    return 1


