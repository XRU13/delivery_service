from redis.asyncio import Redis
from typing import AsyncGenerator

from fastapi import Depends

from sqlalchemy.ext.asyncio import (
	create_async_engine,
	AsyncSession,
	async_sessionmaker,
)

from app.adapters import database
from app.adapters.database.repositories import ParcelRepo
from app.applications.services.parcel_services import ParcelService
from app.utils.settings import RateSettings


class Settings:
	db = database.settings.MySQLSettings()
	celery_settings = database.settings.CelerySettings()
	redis_settings = RateSettings()


class DB:
	engine = create_async_engine(Settings.db.DATABASE_URL)
	async_session_factory = async_sessionmaker(
		bind=engine,
		class_=AsyncSession,
		expire_on_commit=False,
	)


class CeleryDB:
	engine = create_async_engine(Settings.celery_settings.DATABASE_URL)
	async_session_factory = async_sessionmaker(
		bind=engine,
		class_=AsyncSession,
		expire_on_commit=False,
	)


async def get_celery_db_session() -> AsyncGenerator[AsyncSession, None]:
	async with CeleryDB.async_session_factory() as session:
		try:
			yield session
			await session.commit()
		except:
			await session.rollback()
			raise


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
	async with DB.async_session_factory() as session:
		try:
			yield session
			await session.commit()
		except:
			await session.rollback()
			raise


def create_redis_connection() -> Redis:
	return Redis(
		host=Settings.redis_settings.redis_host,
		port=Settings.redis_settings.redis_port,
		db=Settings.redis_settings.redis_db,
		decode_responses=True,
	)


async def create_parcel_repo(
	session: AsyncSession = Depends(get_db_session)
) -> ParcelRepo:
	return ParcelRepo(session=session)


def create_parcel_service(
	parcel_repo: ParcelRepo = Depends(create_parcel_repo),
) -> ParcelService:
	return ParcelService(parcel_repo=parcel_repo)
