from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.booking.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.rooms.router import router as router_hotels

from app.pages.router import router as router_pages
from app.images.router import router as router_images

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from app.config import setting

from redis import asyncio as aioredis

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{setting.REDIS_HOST}:{setting.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)

app.include_router(router_pages)
app.include_router(router_images)

@cache()
async def get_cache():
    return 1

