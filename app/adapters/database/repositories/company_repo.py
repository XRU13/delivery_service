from sqlalchemy import select

from app.applications.dataclasses.dataclasses import Company
from app.applications.interfaces.company_interfaces import ICompanyRepositories


class CompanyRepo(ICompanyRepositories):
	"""
	Реализация репозитория транспортных компаний.
	"""

	def __init__(self, session):
		"""
		Инициализация репозитория с передачей SQLAlchemy-сессии.

		Args:
			session (AsyncSession): Асинхронная сессия SQLAlchemy.
		"""
		self.session = session

	async def create_company(self, company_name: str) -> int:
		"""
        Создаёт новую транспортную компанию и возвращает её ID.

        :param company_name: Название компании
        :return: Уникальный ID созданной компании
        """
		company = Company(name=company_name)
		self.session.add(company)
		await self.session.flush()
		return company.id

	async def get_all_companies(self) -> list[Company]:
		"""
        Возвращает список всех зарегистрированных компаний.

        :return: Список объектов Company
        """
		result = await self.session.execute(select(Company))
		return result.scalars().all()
