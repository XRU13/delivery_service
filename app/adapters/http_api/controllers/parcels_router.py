import logging

from fastapi import APIRouter, Depends, status, Response, Query, Path

from app.adapters.http_api.schemas.schemas import (
	ParcelCreateSchema,
	ParcelResponse,
	ParcelTypeResponse,
	ParcelListResponse,
	ParcelDetailResponse,
	BindCompanyResponseSchema,
	BindCompanySchema,
)
from app.adapters.http_api.settings import (
	create_parcel_service,
	get_or_create_session_id,
)
from app.applications.services.parcel_services import ParcelService

logger = logging.getLogger(__name__)

parcel_router = APIRouter()


@parcel_router.post(
	'/',
	response_model=ParcelResponse,
	status_code=status.HTTP_201_CREATED,
	summary='Создать посылку',
	description='Создаёт новую посылку в рамках пользовательской сессии. '
	            'Если посылка с таким именем уже существует — возвращает её ID.'
)
async def create_parcel(
	response: Response,
	parcel: ParcelCreateSchema,
	parcel_service: ParcelService = Depends(create_parcel_service),
	session_id: str = Depends(get_or_create_session_id),
) -> ParcelResponse:
	"""
    Создание новой посылки. Повторная запись с тем же именем в рамках одной
    сессии не допускается.
    """
	logger.info(
		f'POST /parcels — Регистрация посылки: {parcel.model_dump()} '
		f'(session_id={session_id})')
	parcel_id = await parcel_service.create_parcel(
		name=parcel.name,
		weight=parcel.weight,
		type_id=parcel.type_id,
		content_value_usd=parcel.content_value_usd,
		session_id=session_id,
	)
	logger.info(f'Посылка зарегистрирована: id={parcel_id}')
	return ParcelResponse(parcel_id=parcel_id)


@parcel_router.get(
	'/types',
	response_model=list[ParcelTypeResponse],
	status_code=status.HTTP_200_OK,
	summary='Получить типы посылок',
	description='Возвращает список всех зарегистрированных типов посылок.',
)
async def list_parcel_types(
	parcel_service: ParcelService = Depends(create_parcel_service),
) -> list[ParcelTypeResponse]:
	"""
    Получение всех типов посылок с идентификаторами и названиями.
    """
	logger.info('GET /parcels/types — Получение всех типов посылок')
	types = await parcel_service.get_all_types()
	logger.info(f'Типов найдено: {len(types)}')
	return types


@parcel_router.get(
	'/',
	response_model=list[ParcelListResponse],
	status_code=status.HTTP_200_OK,
	summary='Получить список посылок',
	description='Возвращает список посылок пользователя с возможностью'
	            ' фильтрации и пагинации.',
)
async def list_parcels(
	response: Response,
	type_id: int | None = Query(None, description='Фильтр по типу'),
	has_delivery_cost: bool | None = Query(
		None, description='True — только с рассчитанной стоимостью, False — без'
	),
	limit: int = Query(20, ge=1, le=100),
	offset: int = Query(0, ge=0),
	parcel_service: ParcelService = Depends(create_parcel_service),
	session_id: str = Depends(get_or_create_session_id),
) -> list[ParcelListResponse]:
	"""
    Получение списка посылок пользователя с возможностью фильтрации по типу
    и наличию цены доставки.
    """
	logger.info(
		f'GET /parcels — Список посылок: type_id={type_id}, '
		f'has_cost={has_delivery_cost}, limit={limit}, '
		f'offset={offset}, session_id={session_id}')
	parcels = await parcel_service.list_parcels(
		session_id=session_id,
		type_id=type_id,
		has_delivery_cost=has_delivery_cost,
		limit=limit,
		offset=offset,
	)
	logger.info(f'Посылок найдено: {len(parcels)}')
	return parcels


@parcel_router.get(
	'/{parcel_id}',
	response_model=ParcelDetailResponse,
	status_code=status.HTTP_200_OK,
	summary='Получить посылку по ID',
	description='Возвращает детальную информацию по посылке, если она '
	            'принадлежит текущей сессии.',
)
async def get_parcel(
	response: Response,
	parcel_id: int = Path(..., ge=1),
	parcel_service: ParcelService = Depends(create_parcel_service),
	session_id: str = Depends(get_or_create_session_id),
) -> ParcelDetailResponse:
	"""
    Получение полной информации о конкретной посылке по её ID.
    """
	logger.info(
		f'GET /parcels/{parcel_id} — Получение посылки '
		f'(session_id={session_id})')
	parcel = await parcel_service.get_parcel(
		parcel_id=parcel_id,
		session_id=session_id,
	)
	logger.info(f'Посылка найдена: id={parcel_id}')
	return parcel


@parcel_router.post(
	'/bind_company',
	response_model=BindCompanyResponseSchema,
	status_code=status.HTTP_200_OK,
	summary='Привязать посылку к транспортной компании',
	description='Привязывает посылку к компании, если она ещё'
	            ' не была привязана.',
)
async def bind_parcel_to_company(
	response: Response,
	company_data: BindCompanySchema,
	parcel_service: ParcelService = Depends(create_parcel_service),
) -> BindCompanyResponseSchema:
	"""
    Привязывает посылку к указанной транспортной компании.
    Возвращает ошибку 409, если посылка уже привязана.
    """
	logger.info(
		f'POST /parcels/bind_company — Привязка компании: '
		f'{company_data.model_dump()}')
	result = await parcel_service.bind_company_to_parcel(
		parcel_id=company_data.parcel_id,
		company_id=company_data.company_id,
	)
	logger.info(
		f'Успешная привязка parcel_id={company_data.parcel_id}'
		f' к company_id={company_data.company_id}')
	return result
