import httpx
from redis.asyncio import Redis


class RateService:
    """
    Получает курс USD→RUB и кеширует его в Redis на заданный TTL.
    """

    def __init__(self, redis: Redis, cbr_url: str, ttl_seconds: int = 300):
        self._redis = redis
        self._cbr_url = cbr_url
        self._ttl = ttl_seconds

    async def get_usd_rub_rate(self) -> float:
        # 1. Сначала пробуем взять значение из Redis-кеша
        cached = await self._redis.get("USD_RUB")
        if cached is not None:
            return float(cached)

        # 2. Если в кеше нет, делаем HTTP-запрос к API ЦБ
        async with httpx.AsyncClient() as client:
            resp = await client.get(self._cbr_url, timeout=5.0)
            resp.raise_for_status()
            data = resp.json()

        rate = float(data["Valute"]["USD"]["Value"])

        # 3. Кладём в кеш с истечением ttl_seconds
        await self._redis.set("USD_RUB", rate, ex=self._ttl)
        return rate
