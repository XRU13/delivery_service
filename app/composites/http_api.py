from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI


from app.adapters.http_api.controllers.parcels_router import parcel_router
from app.adapters.http_api.controllers.tasks_router import tasks_router
from app.adapters.http_api.controllers.company_router import company_router

app = FastAPI(
    title='International Delivery Service',
    description='API для сервиса доставки посылок',
    version='1.0.0',
    debug=True,
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
