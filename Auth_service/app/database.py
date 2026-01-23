from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import setting


if setting.MODE == "TEST":
    DATABASE_URL = setting.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = setting.DATABASE_URL
    DATABASE_PARAMS = {}

engin = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = async_sessionmaker(engin, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
