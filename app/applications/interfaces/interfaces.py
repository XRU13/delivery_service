from abc import ABC, abstractmethod

from app.applications.dataclasses.dataclasses import Parcel, ParcelType


class IParcelRepositories(ABC):

	@abstractmethod
	async def create_parcel(
		self,
		name: str,
		weight: float,
		type_id: int,
		content_value_usd: float,
		session_id: str,
		delivery_price: float | None = None,
	) -> int:
		pass

	@abstractmethod
	async def get_by_name_and_session(
		self,
		name: str,
		session_id: str,
	) -> Parcel | None:
		pass

	@abstractmethod
	async def get_all_types(self) -> list[ParcelType]:
		pass

	@abstractmethod
	async def list_by_filters(
		self,
		session_id: str,
		type_id: int | None,
		has_delivery_cost: bool | None,
		limit: int,
		offset: int,
	) -> list[Parcel]:
		pass

	@abstractmethod
	async def get_by_id_and_session(
		self,
		parcel_id: int,
		session_id: str,
	) -> Parcel | None:
		pass

	@abstractmethod
	async def get_unpriced_parcels(self) -> list[Parcel]:
		pass

	@abstractmethod
	async def bind_company_to_parcel(
		self,
		parcel_id: int,
		company_id: int,
	) -> bool:
		pass
