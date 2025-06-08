from uuid import uuid4

from redis.asyncio import Redis
from typing import AsyncGenerator

from fastapi import Depends, Response, Cookie

from sqlalchemy.ext.asyncio import (
	create_async_engine,
	AsyncSession,
	async_sessionmaker,
)

from app.adapters import database
from app.adapters.database.repositories.parcel_repo import ParcelRepo
from app.adapters.database.repositories.company_repo import CompanyRepo
from app.applications.services.company_service import CompanyService
from app.applications.services.parcel_services import ParcelService
from app.utils.constants import CookiesConstants
from app.utils.settings import RateSettings


class Settings:
	"""Объединённые настройки приложения."""
	db = database.settings.MySQLSettings()
	celery_settings = database.settings.CelerySettings()
	redis_settings = RateSettings()


class DB:
	"""Основное подключение к БД приложения."""
	engine = create_async_engine(Settings.db.DATABASE_URL)
	async_session_factory = async_sessionmaker(
		bind=engine,
		class_=AsyncSession,
		expire_on_commit=False,
	)


class CeleryDB:
	"""Подключение к БД для задач Celery."""
	engine = create_async_engine(Settings.celery_settings.DATABASE_URL)
	async_session_factory = async_sessionmaker(
		bind=engine,
		class_=AsyncSession,
		expire_on_commit=False,
	)


async def get_celery_db_session() -> AsyncGenerator[AsyncSession, None]:
	"""
	Асинхронный генератор сессии для задач Celery.
	Используется из фоновых процессов.
	"""
	async with CeleryDB.async_session_factory() as session:
		try:
			yield session
			await session.commit()
		except:
			await session.rollback()
			raise


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
	"""
	Асинхронный генератор сессии SQLAlchemy для FastAPI.
	Открывает транзакцию, коммитит при успешном завершении, иначе откатывает.
	"""
	async with DB.async_session_factory() as session:
		try:
			yield session
			await session.commit()
		except:
			await session.rollback()
			raise


def create_redis_connection() -> Redis:
	"""
	Создаёт подключение к Redis на основе конфигурации.
	"""
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


async def create_company_repo(
	session: AsyncSession = Depends(get_db_session)
) -> CompanyRepo:
	"""
	Провайдер репозитория ParcelRepo для FastAPI DI.
	"""
	return CompanyRepo(session=session)


def create_company_service(
	company_repo: CompanyRepo = Depends(create_company_repo),
) -> CompanyService:
	"""
	Провайдер репозитория CompanyRepo для FastAPI DI.
	"""
	return CompanyService(company_repo=company_repo)


def create_parcel_service(
	parcel_repo: ParcelRepo = Depends(create_parcel_repo),
) -> ParcelService:
	"""
	Провайдер бизнес-сервиса для компаний.
	"""
	return ParcelService(parcel_repo=parcel_repo)


async def get_or_create_session_id(
	response: Response,
	session_id: str | None = Cookie(
		default=None,
		alias=CookiesConstants.SESSION_ID.value,
	),
) -> str:
	"""
	Получает session_id из cookies или создаёт новый,
	устанавливает его в ответ как HttpOnly cookie.

	Используется для связывания посылок с пользователем без авторизации.
	"""
	if session_id is None:
		session_id = uuid4().hex
		response.set_cookie(
			key=CookiesConstants.SESSION_ID.value,
			value=session_id,
			httponly=True,
			max_age=CookiesConstants.MAX_AGE.value,
		)
	return session_id


