from typing import Optional, List

from attr import frozen

from app.adapters.http_api.schemas.schemas import (
	ParcelTypeResponse,
	ParcelListResponse,
	ParcelDetailResponse,
)
from app.applications.interfaces.interfaces import IParcelRepositories
from app.applications.services.errors.errors import NotFoundError
from app.utils.constants import ServiceConstants


@frozen
class ParcelService:
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
		Создаёт новую посылку и возвращает её ID.
		Проверяет существование в рамках одной сессии через репозиторий.
		"""
		existing = await self.parcel_repo.get_by_name_and_session(
			name=name,
			session_id=session_id,
		)
		if existing:
			return existing.id

		parcel = await self.parcel_repo.create_parcel(
			name=name,
			weight=weight,
			type_id=type_id,
			content_value_usd=content_value_usd,
			session_id=session_id,
		)
		return parcel

	async def get_all_types(self) -> List[ParcelTypeResponse]:
		"""
		Получаем все типы посылок
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
		type_id: Optional[int],
		has_delivery_cost: Optional[bool],
		limit: int,
		offset: int,
	) -> List[ParcelListResponse]:
		"""
		Получаем список посылок
		"""
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
						else ServiceConstants.NOT_MEANT
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
		Возвращает детальную информацию по одной посылке,
		либо кидает NotFoundError, если нет.
		"""
		parcel = await self.parcel_repo.get_by_id_and_session(
			parcel_id=parcel_id,
			session_id=session_id,
		)
		if parcel is None:
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
				else ServiceConstants.NOT_MEANT
			),
			created_at=parcel.created_at,
		)