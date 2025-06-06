from fastapi import APIRouter, Depends, status, Response, Query, Path

from app.adapters.http_api.schemas.schemas import (
	ParcelCreateSchema,
	ParcelResponse,
	ParcelTypeResponse,
	ParcelListResponse,
	ParcelDetailResponse,
)
from app.adapters.http_api.settings import (
	create_parcel_service,
	get_or_create_session_id,
)
from app.applications.services.parcel_services import ParcelService

parcel_router = APIRouter()


@parcel_router.post(
	'/',
	response_model=ParcelResponse,
	status_code=status.HTTP_201_CREATED,
)
async def create_parcel(
	response: Response,
	parcel: ParcelCreateSchema,
	parcel_service: ParcelService = Depends(create_parcel_service),
	session_id: str = Depends(get_or_create_session_id),
) -> ParcelResponse:
	"""
	Зарегистрировать новую посылку
	"""
	parcel_id = await parcel_service.create_parcel(
		name=parcel.name,
		weight=parcel.weight,
		type_id=parcel.type_id,
		content_value_usd=parcel.content_value_usd,
		session_id=session_id,
	)
	return ParcelResponse(parcel_id=parcel_id)


@parcel_router.get(
	'/types',
	response_model=list[ParcelTypeResponse],
	status_code=status.HTTP_200_OK,
)
async def list_parcel_types(
	parcel_service: ParcelService = Depends(create_parcel_service),
) -> list[ParcelTypeResponse]:
	"""
	Получить все типы посылок и их ID.
	"""
	return await parcel_service.get_all_types()


@parcel_router.get(
	'/',
	response_model=list[ParcelListResponse],
	status_code=status.HTTP_200_OK,
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
	Список своих посылок с возможностью фильтра и пагинации.
	"""
	return await parcel_service.list_parcels(
		session_id=session_id,
		type_id=type_id,
		has_delivery_cost=has_delivery_cost,
		limit=limit,
		offset=offset,
	)


@parcel_router.get(
	'/{parcel_id}',
	response_model=ParcelDetailResponse,
	status_code=status.HTTP_200_OK,
)
async def get_parcel(
	response: Response,
	parcel_id: int = Path(..., ge=1),
	parcel_service: ParcelService = Depends(create_parcel_service),
	session_id: str = Depends(get_or_create_session_id),
) -> ParcelDetailResponse:
	"""
	Получить данные о посылке по ее ID.
	"""
	return await parcel_service.get_parcel(
		parcel_id=parcel_id,
		session_id=session_id,
	)
