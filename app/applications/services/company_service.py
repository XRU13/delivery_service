from dataclasses import dataclass

from app.adapters.http_api.schemas.schemas import CompanyResponse
from app.applications.interfaces.company_interfaces import ICompanyRepositories


@dataclass(frozen=True)
class CompanyService:
	company_repo: ICompanyRepositories

	async def create_company(self, company_name: str) -> int:
		"""
        Создаёт новую компанию и возвращает её ID.
        """
		return await self.company_repo.create_company(company_name=company_name)

	async def get_all_companies(self) -> list[CompanyResponse]:
		"""
		Возвращает список всех зарегистрированных компаний.
		"""
		companies = await self.company_repo.get_all_companies()
		return [CompanyResponse(
			id=company.id,
			name=company.name,
		) for company in companies]
