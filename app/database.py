from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import setting

engin = create_async_engine(setting.DB_URL)

async_session_maker = sessionmaker(engin, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
