import logging

from fastapi import APIRouter
from starlette import status

from app.tasks.price_tasks import update_delivery_prices

logger = logging.getLogger(__name__)

tasks_router = APIRouter()


@tasks_router.post(
	'/price-update',
	status_code=status.HTTP_202_ACCEPTED,
	summary='Обновить стоимость посылок',
description=(
        'Запускает фоновую задачу (через Celery) по пересчёту стоимости'
        ' доставки для всех посылок, у которых ещё не установлена цена.'
    )
)
async def trigger_update_delivery_prices():
	"""
    Триггер для асинхронного обновления цен доставки.

    Запускает задачу Celery `update_delivery_prices`,
    которая рассчитывает стоимость доставки для всех посылок без установленной
    цены и сохраняет её в базу.
    """
	task = update_delivery_prices.delay()
	logger.info(f'Задача Celery отправлена: task_id={task.id}')
	return {'status': 'submitted', 'task_id': task.id}
