from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from redis.asyncio import Redis
from typing import AsyncGenerator

from app.adapters.database.settings import MySQLSettings
from app.utils.settings import RateSettings

# Загружаем настройки
db_settings = MySQLSettings()
redis_settings = RateSettings()

# Создаём асинхронный SQLAlchemy-движок
engine = create_async_engine(db_settings.DATABASE_URL, future=True, echo=False)
# Создаём фабрику сессий
async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_celery_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный генератор сессий базы данных для задач Celery.

    Используется в фоновом режиме, чтобы открыть транзакцию, выполнить работу
    и закрыть сессию.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise

def get_celery_redis() -> Redis:
    """
    Создаёт Redis-клиент для использования внутри Celery-задач.

    Возвращает:
        Redis: Асинхронный Redis-клиент.
    """
    return Redis(
        host=redis_settings.redis_host,
        port=redis_settings.redis_port,
        db=redis_settings.redis_db,
        decode_responses=True,
    )
