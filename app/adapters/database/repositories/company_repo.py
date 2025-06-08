from sqlalchemy import select

from app.applications.dataclasses.dataclasses import Company
from app.applications.interfaces.company_interfaces import ICompanyRepositories


class CompanyRepo(ICompanyRepositories):

	def __init__(self, session):
		self.session = session

	async def create_company(self, company_name: str) -> int:
		company = Company(name=company_name)
		self.session.add(company)
		await self.session.flush()
		return company.id

	async def get_all_companies(self) -> list[Company]:
		result = await self.session.execute(select(Company))
		return result.scalars().all()
