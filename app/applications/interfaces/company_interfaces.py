from abc import ABC, abstractmethod
from app.applications.dataclasses.dataclasses import Company


class ICompanyRepositories(ABC):
    """
    Интерфейс репозитория компаний.

    Определяет контракт взаимодействия с хранилищем данных для компаний.
    """

    @abstractmethod
    async def create_company(self, company_name: str) -> int:
        """
        Создаёт новую транспортную компанию и возвращает её ID.

        :param company_name: Название компании
        :return: Уникальный ID созданной компании
        """
        pass

    @abstractmethod
    async def get_all_companies(self) -> list[Company]:
        """
        Возвращает список всех зарегистрированных компаний.

        :return: Список объектов Company
        """
        pass
