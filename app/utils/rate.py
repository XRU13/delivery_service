import logging

import httpx
from redis.asyncio import Redis

logger = logging.getLogger(__name__)


class RateService:
	"""
    Сервис получения и кеширования валютного курса USD→RUB.

    Работает следующим образом:
    1. Пытается получить курс из Redis.
    2. Если в кеше нет — делает запрос к API ЦБ РФ.
    3. После получения сохраняет курс в Redis на заданное TTL-время.
    """

	def __init__(self, redis: Redis, cbr_url: str, ttl_seconds: int = 300):
		self._redis = redis
		self._cbr_url = cbr_url
		self._ttl = ttl_seconds

	async def get_usd_rub_rate(self) -> float:
		"""
        Возвращает курс USD→RUB, сначала проверяя Redis,
        а при отсутствии данных — запрашивает у API ЦБ.
        """
		# Сначала пробуем взять значение из Redis-кеша
		cached = await self._redis.get('USD_RUB')
		if cached is not None:
			return float(cached)

		# Если в кеше нет, делаем HTTP-запрос к API ЦБ
		try:
			async with httpx.AsyncClient() as client:
				resp = await client.get(self._cbr_url, timeout=5.0)
				resp.raise_for_status()
				data = resp.json()
		except Exception as e:
			logger.exception(f'Ошибка при получении курса с {self._cbr_url}')
			raise

		rate = float(data['Valute']['USD']['Value'])
		logger.info(f'Курс USD→RUB получен от ЦБ: {rate}')

		# Кладём в кеш с истечением ttl_seconds
		await self._redis.set('USD_RUB', rate, ex=self._ttl)
		return rate
