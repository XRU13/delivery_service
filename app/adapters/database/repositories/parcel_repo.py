import datetime

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.applications.dataclasses.dataclasses import Parcel, ParcelType
from app.applications.interfaces.parcel_interfaces import IParcelRepositories


class ParcelRepo(IParcelRepositories):
    """
    Репозиторий для работы с посылками в базе данных.
    """

    def __init__(self, session):
        """
        Инициализация репозитория с асинхронной SQLAlchemy-сессией.

        :param session: Асинхронная сессия SQLAlchemy.
        """
        self.session = session

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
        parcel = Parcel(
                session_id=session_id,
                name=name,
                weight=weight,
                type_id=type_id,
                content_value_usd=content_value_usd,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now()
            )
        self.session.add(parcel)
        await self.session.flush()
        return parcel.id

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
        stmt = select(Parcel).where(
            Parcel.name == name,
            Parcel.session_id == session_id
        )

        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_types(self) -> list[ParcelType]:
        """
        Получает список всех типов посылок.

        :return: Список ParcelType
        """
        stmt = select(ParcelType)
        result = await self.session.execute(stmt)
        return result.scalars().all()

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
        stmt = (
            select(Parcel)
            .options(selectinload(Parcel.type))
            .where(Parcel.session_id == session_id)
        )

        if type_id is not None:
            stmt = stmt.where(Parcel.type_id == type_id)

        if has_delivery_cost is True:
            stmt = stmt.where(Parcel.delivery_price.isnot(None))
        elif has_delivery_cost is False:
            stmt = stmt.where(Parcel.delivery_price.is_(None))

        stmt = stmt.order_by(Parcel.created_at.desc())
        stmt = stmt.limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return result.scalars().all()

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
        stmt = (
            select(Parcel)
            .options(selectinload(Parcel.type))
            .where(
                Parcel.id == parcel_id,
                Parcel.session_id == session_id
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_unpriced_parcels(self) -> list[Parcel]:
        """
        Возвращает все посылки, у которых не рассчитана стоимость доставки.

        :return: Список посылок без delivery_price
        """
        stmt = (
            select(Parcel)
            .where(Parcel.delivery_price.is_(None))
            .options(selectinload(Parcel.type))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

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
        stmt = (
            update(Parcel)
            .where(
                Parcel.id == parcel_id,
                Parcel.company_id.is_(None),
            )
            .values(company_id=company_id)
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0
