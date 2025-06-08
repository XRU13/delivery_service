import logging
import os
from celery import Celery
from celery.signals import worker_ready, task_prerun, task_postrun, task_failure

logger = logging.getLogger(__name__)

broker = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
backend = os.getenv('CELERY_RESULT_BACKEND', broker)

celery_app = Celery(
	'delivery_service',
	broker=broker,
	backend=backend,
	include=['app.tasks.price_tasks'],
)

celery_app.conf.worker_pool = os.getenv(
	'CELERY_CUSTOM_WORKER_POOL',
	'celery_aio_pool.pool:AsyncIOPool'
)

celery_app.conf.beat_schedule = {
	'update_delivery_prices_every_5_minutes': {
		'task': 'app.tasks.price_tasks.update_delivery_prices',
		'schedule': 300.0,
	},
}
celery_app.conf.timezone = 'UTC'
celery_app.conf.enable_utc = True


@worker_ready.connect
def on_worker_ready(sender, **kwargs):
	logger.info('Celery worker is ready')


@task_prerun.connect
def on_task_start(task_id, task, *args, **kwargs):
	logger.info(f'Задача запущена: {task.name} [task_id={task_id}]')


@task_postrun.connect
def on_task_finish(task_id, task, retval, **kwargs):
	logger.info(f'Задача завершена: {task.name} [task_id={task_id}]')


@task_failure.connect
def on_task_failure(task_id, exception, traceback, task, **kwargs):
	logger.error(
		f'Ошибка в задаче {task.name} [task_id={task_id}]: {exception}')
