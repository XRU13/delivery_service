from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, status, Request, Response, Query, Path

from app.adapters.http_api.schemas.schemas import (
	ParcelCreateSchema,
	ParcelResponse,
	ParcelTypeResponse,
	ParcelListResponse,
	ParcelDetailResponse,
)
from app.adapters.http_api.settings import create_parcel_service
from app.applications.services.parcel_services import ParcelService
from app.utils.constants import CookiesConstants

parcel_router = APIRouter()


@parcel_router.post(
	'/',
	response_model=ParcelResponse,
	status_code=status.HTTP_201_CREATED,
)
async def create_parcel(
	request: Request,
	response: Response,
	parcel: ParcelCreateSchema,
	parcel_service: ParcelService = Depends(create_parcel_service),
) -> ParcelResponse:
	"""
	Зарегистрировать новую посылку
	"""
	session_id = request.cookies.get(CookiesConstants.SESSION_ID.value)
	if not session_id:
		session_id = uuid4().hex

		response.set_cookie(
			key=CookiesConstants.SESSION_ID.value,
			value=session_id,
			httponly=True,
			max_age=CookiesConstants.MAX_AGE.value
		)
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
	response_model=List[ParcelTypeResponse],
	status_code=status.HTTP_200_OK,
)
async def list_parcel_types(
	parcel_service: ParcelService = Depends(create_parcel_service),
) -> List[ParcelTypeResponse]:
	"""
	Получить все типы посылок и их ID.
	"""
	return await parcel_service.get_all_types()


@parcel_router.get(
	'/',
	response_model=List[ParcelListResponse],
	status_code=status.HTTP_200_OK,
)
async def list_parcels(
	request: Request,
	response: Response,
	type_id: Optional[int] = Query(None, description="Фильтр по типу"),
	has_delivery_cost: Optional[bool] = Query(
		None, description="True — только с рассчитанной стоимостью, False — без"
	),
	limit: int = Query(20, ge=1, le=100),
	offset: int = Query(0, ge=0),
	parcel_service: ParcelService = Depends(create_parcel_service),
) -> List[ParcelListResponse]:
	"""
	Список своих посылок с возможностью фильтра и пагинации.
	"""
	session_id = request.cookies.get(CookiesConstants.SESSION_ID.value)
	if not session_id:
		session_id = uuid4().hex
		response.set_cookie(
			CookiesConstants.SESSION_ID.value, session_id, httponly=True)

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
	request: Request,
	response: Response,
	parcel_id: int = Path(..., ge=1),
	parcel_service: ParcelService = Depends(create_parcel_service),
) -> ParcelDetailResponse:
	"""
	Получить данные о посылке по ее ID.
	"""
	session_id = request.cookies.get(CookiesConstants.SESSION_ID.value)
	if not session_id:
		session_id = uuid4().hex
		response.set_cookie(
			CookiesConstants.SESSION_ID.value, session_id, httponly=True)

	return await parcel_service.get_parcel(
		parcel_id=parcel_id,
		session_id=session_id,
	)
