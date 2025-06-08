from fastapi import APIRouter, Depends, status
from app.adapters.http_api.schemas.schemas import (
    CompanyCreateSchema,
    CompanyResponse,
)
from app.adapters.http_api.settings import create_company_service
from app.applications.services.company_service import CompanyService

company_router = APIRouter()


@company_router.post(
    '/',
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Создать транспортную компанию',
)
async def create_company(
    company: CompanyCreateSchema,
    company_service: CompanyService = Depends(create_company_service),
) -> CompanyResponse:
    company_id = await company_service.create_company(company_name=company.name)
    return CompanyResponse(id=company_id, name=company.name)


@company_router.get(
    '/',
    response_model=list[CompanyResponse],
    status_code=status.HTTP_200_OK,
    summary='Получить список всех компаний',
)
async def list_companies(
	company_service: CompanyService = Depends(create_company_service),
) -> list[CompanyResponse]:
    return await company_service.get_all_companies()
