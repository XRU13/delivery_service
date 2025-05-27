import attr
from datetime import datetime
from typing import Optional


@attr.dataclass
class Parcel:
	session_id: str
	name: str
	weight: float
	type_id: int
	content_value_usd: float
	created_at: datetime
	updated_at: datetime
	delivery_price: Optional[float] = None
	id: Optional[int] = None


@attr.dataclass
class ParcelType:
	name: str
	id: Optional[int] = None
