import datetime
from typing import List

from app.applications.dataclasses.dataclasses import Parcel
from app.adapters.database.repositories import ParcelRepo
from app.utils.rate import RateService


class PriceUpdateService:
	"""
	Сервис, который обновляет стоимость доставки для необработанных посылок.
	"""

	def __init__(self, parcel_repo: ParcelRepo, rate_service: RateService):
		self._parcel_repo = parcel_repo
		self._rate_service = rate_service

	async def update_all(self) -> None:
		rate = await self._rate_service.get_usd_rub_rate()
		parcels: List[Parcel] = await self._parcel_repo.get_unpriced_parcels()

		for parcel in parcels:
			parcel.delivery_price = (
				# формула расчета стоимости
				(parcel.weight * 0.5 + parcel.content_value_usd * 0.01) * rate)
			parcel.updated_at = datetime.datetime.now()
