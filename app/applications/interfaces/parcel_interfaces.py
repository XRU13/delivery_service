from abc import ABC, abstractmethod
from app.applications.dataclasses.dataclasses import Parcel, ParcelType


class IParcelRepositories(ABC):
    """
    Интерфейс репозитория посылок.

    Определяет контракт для работы с хранилищем посылок и их типами.
    Поддерживает фильтрацию, поиск, создание и привязку к компаниям.
    """

    @abstractmethod
    async def create_parcel(
        self,
        name: str,
        weight: float,
        type_id: int,
        content_value_usd: float,
        session_id: str,
        delivery_price: float | None = None,
    ) -> int:
        """
        Создаёт новую посылку и возвращает её ID.

        :param name: Название посылки
        :param weight: Вес в килограммах
        :param type_id: ID типа посылки
        :param content_value_usd: Стоимость содержимого в USD
        :param session_id: Идентификатор пользовательской сессии
        :param delivery_price: Стоимость доставки (опционально)
        :return: ID новой посылки
        """
        pass

    @abstractmethod
    async def get_by_name_and_session(
        self,
        name: str,
        session_id: str,
    ) -> Parcel | None:
        """
        Возвращает посылку по имени и сессии, если найдена.

        :param name: Название посылки
        :param session_id: Идентификатор сессии
        :return: Объект Parcel или None
        """
        pass

    @abstractmethod
    async def get_all_types(self) -> list[ParcelType]:
        """
        Получает список всех типов посылок.

        :return: Список ParcelType
        """
        pass

    @abstractmethod
    async def list_by_filters(
        self,
        session_id: str,
        type_id: int | None,
        has_delivery_cost: bool | None,
        limit: int,
        offset: int,
    ) -> list[Parcel]:
        """
        Возвращает отфильтрованный список посылок пользователя.

        :param session_id: Сессия пользователя
        :param type_id: Фильтр по типу (если указан)
        :param has_delivery_cost: True/False для фильтрации по цене доставки
        :param limit: Ограничение количества результатов
        :param offset: Смещение для пагинации
        :return: Список посылок
        """
        pass

    @abstractmethod
    async def get_by_id_and_session(
        self,
        parcel_id: int,
        session_id: str,
    ) -> Parcel | None:
        """
        Получает посылку по её ID и сессии пользователя.

        :param parcel_id: Уникальный идентификатор посылки
        :param session_id: Идентификатор сессии пользователя
        :return: Parcel или None
        """
        pass

    @abstractmethod
    async def get_unpriced_parcels(self) -> list[Parcel]:
        """
        Возвращает все посылки, у которых не рассчитана стоимость доставки.

        :return: Список посылок без delivery_price
        """
        pass

    @abstractmethod
    async def bind_company_to_parcel(
        self,
        parcel_id: int,
        company_id: int,
    ) -> bool:
        """
        Привязывает транспортную компанию к посылке.

        :param parcel_id: ID посылки
        :param company_id: ID компании
        :return: True, если привязка успешна; False, если уже привязана
        """
        pass
