import logging

from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, status

from app.adapters.http_api.controllers.parcels_router import parcel_router
from app.adapters.http_api.controllers.tasks_router import tasks_router
from app.adapters.http_api.controllers.company_router import company_router
from app.logging_config import setup_logging

# Настройка логирования
setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
	logger.info('Сервис доставки запущен')
	yield
	logger.info('Сервис доставки остановлен')


app = FastAPI(
	title='International Delivery Service',
	description='API для сервиса доставки посылок',
	version='1.0.0',
	debug=True,
	lifespan=lifespan,
)

app.include_router(parcel_router, prefix='/parcels', tags=['parcels'])
app.include_router(tasks_router, prefix='/tasks', tags=['tasks'])
app.include_router(company_router, prefix='/company', tags=['company'])

app.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*'],
)


@app.get(
	'/',
	summary='Корневой endpoint API',
	description='Служебный endpoint для проверки доступности и состояния сервиса доставки.',
	response_description='Расширенная информация о состоянии API',
	status_code=200,
	tags=['service']
)
async def root():
	"""
	Возвращает информацию о состоянии сервиса, версии API и времени сервера.
	"""
	return {
		'status': status.HTTP_200_OK,
		'version': app.version,
		'server_time_utc': datetime.now(timezone.utc).isoformat(),
		'environment': 'production'
	}
