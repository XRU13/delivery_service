import datetime
import logging

from app.adapters.database.repositories.parcel_repo import ParcelRepo
from app.applications.dataclasses.dataclasses import Parcel
from app.utils.rate import RateService

logger = logging.getLogger(__name__)

class PriceUpdateService:
	"""
    Сервис, который рассчитывает и обновляет стоимость доставки
    для всех посылок, у которых она ещё не задана.

    Формула:
        (вес * 0.5 + стоимость содержимого * 0.01) * текущий курс USD→RUB

    Курс валюты берётся из внешнего API ЦБ РФ (с кешированием в Redis).
    """

	def __init__(self, parcel_repo: ParcelRepo, rate_service: RateService):
		"""
        :param parcel_repo: Репозиторий для работы с посылками
        :param rate_service: Сервис получения актуального курса валют
        """
		self._parcel_repo = parcel_repo
		self._rate_service = rate_service

	async def update_all(self) -> None:
		"""
        Запускает массовое обновление стоимости доставки
        для всех посылок без установленной цены.
        """
		logger.info(
			'Запуск обновления стоимости доставки для необработанных посылок')

		# Получаем текущий курс USD/RUB
		rate = await self._rate_service.get_usd_rub_rate()
		logger.info(f'Текущий курс USD/RUB: {rate}')

		# Загружаем все посылки, у которых не рассчитана стоимость доставки
		parcels: list[Parcel] = await self._parcel_repo.get_unpriced_parcels()
		logger.info(f'Найдено посылок без цены доставки: {len(parcels)}')

		updated_count = 0

		# Рассчитываем стоимость и обновляем временную метку
		for parcel in parcels:
			parcel.delivery_price = (
				# формула расчета стоимости
				(parcel.weight * 0.5 + parcel.content_value_usd * 0.01) * rate)
			parcel.updated_at = datetime.datetime.now()
			updated_count += 1

		logger.info(f'Обновление завершено. Обновлено посылок: {updated_count}')
