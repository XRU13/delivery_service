from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from redis.asyncio import Redis
from typing import AsyncGenerator

from app.adapters.database.settings import MySQLSettings
from app.utils.settings import RateSettings

db_settings = MySQLSettings()
redis_settings = RateSettings()

engine = create_async_engine(db_settings.DATABASE_URL, future=True, echo=False)
async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_celery_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise

def get_celery_redis() -> Redis:
    return Redis(
        host=redis_settings.redis_host,
        port=redis_settings.redis_port,
        db=redis_settings.redis_db,
        decode_responses=True,
    )
