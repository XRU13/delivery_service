import logging
from dataclasses import dataclass

from fastapi import HTTPException
from starlette import status

from app.adapters.http_api.schemas.schemas import (
	ParcelTypeResponse,
	ParcelListResponse,
	ParcelDetailResponse, BindCompanyResponseSchema,
)
from app.applications.interfaces.parcel_interfaces import IParcelRepositories
from app.applications.services.errors.errors import NotFoundError
from app.utils.constants import ParcelsConstants

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ParcelService:
	"""
	Сервис для управления посылками: создание, получение, фильтрация,
	привязка к транспортным компаниям и отображение информации.
	"""

	parcel_repo: IParcelRepositories

	async def create_parcel(
		self,
		name: str,
		weight: float,
		type_id: int,
		content_value_usd: float,
		session_id: str,
	) -> int:
		"""
		Создать новую посылку или вернуть ID существующей,
		если посылка с таким именем уже существует в рамках текущей сессии.

		:param name: Название посылки
		:param weight: Вес посылки в кг
		:param type_id: Идентификатор типа посылки
		:param content_value_usd: Стоимость содержимого в долларах
		:param session_id: Идентификатор пользовательской сессии
		:return: ID посылки
		"""
		# Проверяем, существует ли уже посылка с таким именем
		# в рамках сессии пользователя
		existing = await self.parcel_repo.get_by_name_and_session(
			name=name,
			session_id=session_id,
		)
		if existing:
			logger.info(f'Посылка уже существует: id={existing.id}')
			return existing.id

		# Если не существует — создаём новую посылку
		parcel = await self.parcel_repo.create_parcel(
			name=name,
			weight=weight,
			type_id=type_id,
			content_value_usd=content_value_usd,
			session_id=session_id,
		)
		return parcel

	async def get_all_types(self) -> list[ParcelTypeResponse]:
		"""
		Получить все доступные типы посылок.

		:return: Список объектов ParcelTypeResponse
		"""
		parcel_types = await self.parcel_repo.get_all_types()
		return [
			ParcelTypeResponse(
				type_id=parcel_type.id,
				name=parcel_type.name,
			) for parcel_type in parcel_types
		]

	async def list_parcels(
		self,
		session_id: str,
		type_id: int | None,
		has_delivery_cost: bool | None,
		limit: int,
		offset: int,
	) -> list[ParcelListResponse]:
		"""
		Получить список посылок текущей сессии с возможностью фильтрации
		и пагинации.

		:param session_id: Идентификатор сессии
		:param type_id: Тип посылки (опционально)
		:param has_delivery_cost: Только с/без стоимости доставки (опционально)
		:param limit: Ограничение на количество элементов
		:param offset: Смещение для пагинации
		:return: Список ParcelListResponse
		"""
		# Получаем посылки из репозитория с применением фильтров
		parcels = await self.parcel_repo.list_by_filters(
			session_id=session_id,
			type_id=type_id,
			has_delivery_cost=has_delivery_cost,
			limit=limit,
			offset=offset,
		)
		response = []
		for parcel in parcels:
			response.append(
				ParcelListResponse(
					parcel_id=parcel.id,
					name=parcel.name,
					weight=parcel.weight,
					type_id=parcel.type_id,
					type_name=parcel.type.name,
					content_value_usd=parcel.content_value_usd,
					delivery_price=(
						parcel.delivery_price
						if parcel.delivery_price is not None
						else ParcelsConstants.NOT_MEANT.value
					),
					created_at=parcel.created_at,
				)
			)
		return response

	async def get_parcel(
		self,
		parcel_id: int,
		session_id: str,
	) -> ParcelDetailResponse:
		"""
		Получить детальную информацию о посылке по ID и session_id.

		Если не найдена — возбуждается исключение NotFoundError.

		:param parcel_id: ID посылки
		:param session_id: Идентификатор сессии
		:return: Объект ParcelDetailResponse
		"""
		# Пытаемся найти посылку по ID и session_id
		parcel = await self.parcel_repo.get_by_id_and_session(
			parcel_id=parcel_id,
			session_id=session_id,
		)

		# Если не нашли — логируем и выбрасываем исключение
		if parcel is None:
			logger.warning(
				f'Посылка не найдена: id={parcel_id}, session_id={session_id}')
			raise NotFoundError(parcel_id=parcel_id)

		return ParcelDetailResponse(
			parcel_id=parcel.id,
			name=parcel.name,
			weight=parcel.weight,
			type_id=parcel.type_id,
			type_name=parcel.type.name,
			content_value_usd=parcel.content_value_usd,
			delivery_price=(
				parcel.delivery_price
				if parcel.delivery_price is not None
				else ParcelsConstants.NOT_MEANT.value
			),
			created_at=parcel.created_at,
		)

	async def bind_company_to_parcel(
		self,
		parcel_id: int,
		company_id: int,
	) -> BindCompanyResponseSchema:
		"""
		Привязать посылку к компании, если она ещё не привязана.

		Если привязка уже существует — возбуждается HTTP 409.

		:param parcel_id: ID посылки
		:param company_id: ID транспортной компании
		:return: Подтверждение в виде BindCompanyResponseSchema
		"""

		# Пытаемся выполнить привязку.
		# Репозиторий вернёт None, если посылка уже привязана.
		parcel = await self.parcel_repo.bind_company_to_parcel(
			parcel_id=parcel_id,
			company_id=company_id,
		)
		# Если привязка не выполнена — значит уже была, возвращаем 409
		if not parcel:
			logger.warning(f'Посылка уже привязана: parcel_id={parcel_id}')
			raise HTTPException(
				status_code=status.HTTP_409_CONFLICT,
				detail='Посылка уже привязана к компании',
			)
		return BindCompanyResponseSchema()
