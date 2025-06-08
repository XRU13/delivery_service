from abc import ABC, abstractmethod

from app.applications.dataclasses.dataclasses import Company


class ICompanyRepositories(ABC):

	@abstractmethod
	async def create_company(self, company_name: str) -> int:
		pass

	@abstractmethod
	async def get_all_companies(self) -> list[Company]:
		pass
