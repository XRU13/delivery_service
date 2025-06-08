import logging
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

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


@app.get('/')
async def root():
	return {'message': 'Добро пожаловать в API сервиса доставки'}
