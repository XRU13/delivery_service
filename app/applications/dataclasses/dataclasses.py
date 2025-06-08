from dataclasses import dataclass
from datetime import datetime


@dataclass
class Parcel:
	"""
	Доменная модель посылки.

	Используется в бизнес-логике и задачах, абстрагируясь от ORM-модели.
	"""
	session_id: str
	name: str
	weight: float
	type_id: int
	content_value_usd: float
	created_at: datetime
	updated_at: datetime
	delivery_price: float | None = None
	id: int | None = None
	company_id: int | None = None


@dataclass
class ParcelType:
	"""
	Доменная модель типа посылки.
	"""
	name: str
	id: int | None = None


@dataclass
class Company:
	"""
	Доменная модель транспортной компании.
	"""
	name: str
	id: int | None = None
