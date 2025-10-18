import asyncio
import time
from contextlib import asynccontextmanager
from datetime import date
from typing import Optional

import sentry_sdk
from fastapi import Depends, FastAPI, Query, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from redis import Redis
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.bookings.router import router as bookings_router
from app.config import settings
from app.database import engine
from app.hotels.rooms.models import Rooms
from app.hotels.rooms.router import router as rooms_router
from app.hotels.router import router as hotels_router
from app.logger import logger
from app.pages.router import router as pages_router
from app.users.models import Users
from app.users.router import router as users_router

sentry_sdk.init(
    dsn=settings.DSN,
    traces_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("соединение с redis начато")
    try:
        redis = aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
        )
        # Проверяем подключение к Redis
        await redis.ping()
        FastAPICache.init(RedisBackend(redis), prefix="cache")
        logger.info("Redis подключен успешно")
    except Exception as e:
        logger.error(f"Ошибка подключения к Redis: {e}")

    yield

    logger.info("соединение с redis закрыто")
    try:
        await redis.close()
    except:
        pass


app = FastAPI(lifespan=lifespan)

# Подключаем роутеры
app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(pages_router)


@app.get("/")
async def hi():
    return {"message": "hellow"}


# Создаем админку
admin = Admin(app, engine, authentication_backend=authentication_backend)

# Импортируем и регистрируем views
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)

instrumentator.instrument(app).expose(app)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info("Request handling time", extra={"process_time": round(process_time, 4)})
    return response
