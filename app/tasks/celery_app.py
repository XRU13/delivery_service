import os
from celery import Celery

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
