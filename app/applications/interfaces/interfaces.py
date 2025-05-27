from abc import ABC, abstractmethod
from typing import Optional, List

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
		delivery_price: Optional[float] = None,
	) -> int:
		pass

	@abstractmethod
	async def get_by_name_and_session(
		self,
		name: str,
		session_id: str,
	) -> Optional[Parcel]:
		pass

	@abstractmethod
	async def get_all_types(self) -> List[ParcelType]:
		pass

	@abstractmethod
	async def list_by_filters(
		self,
		session_id: str,
		type_id: Optional[int],
		has_delivery_cost: Optional[bool],
		limit: int,
		offset: int,
	) -> List[Parcel]:
		pass

	@abstractmethod
	async def get_by_id_and_session(
		self,
		parcel_id: int,
		session_id: str,
	) -> Optional[Parcel]:
		pass

	@abstractmethod
	async def get_unpriced_parcels(self) -> List[Parcel]:
		pass

