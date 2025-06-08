from dataclasses import dataclass
from datetime import datetime


@dataclass
class Parcel:
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
	name: str
	id: int | None = None


@dataclass
class Company:
	name: str
	id: int | None = None
