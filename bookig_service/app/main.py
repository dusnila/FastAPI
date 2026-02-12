from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import time

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from sqladmin import Admin
from fastapi_versioning import VersionedFastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin
from app.booking.router import router as router_bookings
from app.config import setting
from app.database import engin
from app.hotels.rooms.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.logger import logger
from prometheus_fastapi_instrumentator import Instrumentator


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"]
)


@asynccontextmanager
async def lifespan(app_instance: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{setting.REDIS_HOST}:{setting.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")

    instrumentator.expose(app_instance)

    yield


app = FastAPI(
    lifespan=lifespan,
    title="Booking Service",
)


app.include_router(router_bookings)
app.include_router(router_hotels)

app.include_router(router_pages)
app.include_router(router_images)


@cache()
async def get_cache():
    return 1


app = VersionedFastAPI(app,
    version_format="{major}",
    prefix_format="/v{major}",
    root_path="/booking"
)

app.add_middleware(SessionMiddleware, secret_key="some_secret")

instrumentator.instrument(app).expose(app, endpoint="/metrics", include_in_schema=True)


admin = Admin(app, engin, authentication_backend=authentication_backend, base_url="/admin")

admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "process_time" : round(process_time, 4)
    })
    return response

app.mount("/static", StaticFiles(directory="app/static"), "static")