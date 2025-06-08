import asyncio
import logging

from app.tasks.celery_app import celery_app
from app.adapters.database.repositories.parcel_repo import ParcelRepo
from app.applications.services.price_update_service import PriceUpdateService
from app.tasks.settings import get_celery_redis, get_celery_db_session
from app.utils.rate import RateService

logger = logging.getLogger(__name__)


@celery_app.task(name='app.tasks.price_tasks.update_delivery_prices')
def update_delivery_prices():
    """
    Точка входа для задачи Celery.
    Запускает асинхронную функцию обновления стоимости доставки.
    """
    logger.info('Running update_delivery_prices task...')
    try:
        asyncio.run(_update_delivery_prices_async())
        logger.info('Celery: задача update_delivery_prices успешно завершена')
    except Exception as e:
        logger.exception(f'Ошибка в задаче update_delivery_prices: {e}')


async def _update_delivery_prices_async():
    """
    Асинхронное обновление стоимости доставки для посылок без цены.
    Включает:
    - подключение к Redis
    - получение курса USD/RUB
    - перебор всех сессий базы Celery и обновление цен
    """
    redis = get_celery_redis()
    rate_svc = RateService(
        redis,
        cbr_url='https://www.cbr-xml-daily.ru/daily_json.js',
        ttl_seconds=300,
    )

    async for session in get_celery_db_session():
        repo = ParcelRepo(session=session)
        updater = PriceUpdateService(parcel_repo=repo, rate_service=rate_svc)
        await updater.update_all()

    await redis.close()
