import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.applications.dataclasses.dataclasses import Parcel, ParcelType
from app.applications.interfaces.interfaces import IParcelRepositories


class ParcelRepo(IParcelRepositories):

    def __init__(self, session):
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
        Создает посылку
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
        Возвращает посылку по имени и session_id, или None, если не найдена.
        """
        stmt = select(Parcel).where(
            Parcel.name == name,
            Parcel.session_id == session_id
        )

        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_types(self) -> list[ParcelType]:
        """
        Возвращает все типы посылок.
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
        Возвращает отфильтрованный список посылок.
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
        Возвращает один объект Parcel по его id и session_id,
        или None, если не найден.
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
        Возвращает все посылки без стоимости.
        """
        stmt = (
            select(Parcel)
            .where(Parcel.delivery_price.is_(None))
            .options(selectinload(Parcel.type))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
