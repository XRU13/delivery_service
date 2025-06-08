import logging

from fastapi import APIRouter, Depends, status
from app.adapters.http_api.schemas.schemas import (
    CompanyCreateSchema,
    CompanyResponse,
)
from app.adapters.http_api.settings import create_company_service
from app.applications.services.company_service import CompanyService

logger = logging.getLogger(__name__)
company_router = APIRouter()


@company_router.post(
	'/',
	response_model=CompanyResponse,
	status_code=status.HTTP_201_CREATED,
	summary='Создать транспортную компанию',
	description='Создаёт новую транспортную компанию с заданным именем.',
)
async def create_company(
	company: CompanyCreateSchema,
	company_service: CompanyService = Depends(create_company_service),
) -> CompanyResponse:
	"""
    Создание новой транспортной компании.

    Возвращает ID и имя зарегистрированной компании.
    """
	company_id = await company_service.create_company(company_name=company.name)
	logger.info(f'Компания создана с ID: {company_id}')
	return CompanyResponse(id=company_id, name=company.name)


@company_router.get(
	'/',
	response_model=list[CompanyResponse],
	status_code=status.HTTP_200_OK,
	summary='Получить список всех компаний',
	description='Возвращает список всех зарегистрированных '
	            'транспортных компаний.',
)
async def list_companies(
	company_service: CompanyService = Depends(create_company_service),
) -> list[CompanyResponse]:
	"""
    Получение списка всех транспортных компаний.
    """
	companies = await company_service.get_all_companies()
	logger.info(f'Найдено компаний: {len(companies)}')
	return companies
