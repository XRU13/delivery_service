from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class ParcelTypeBase(BaseModel):
	name: str = Field(..., min_length=1, max_length=50)


class ParcelType(ParcelTypeBase):
	id: int

	model_config = {
		'from_attributes': True,
	}


class ParcelBaseSchema(BaseModel):
	name: str = Field(..., min_length=1, max_length=100)
	weight: float = Field(..., gt=0)
	type_id: int = Field(..., gt=0)
	content_value_usd: float = Field(..., gt=0)


class ParcelCreateSchema(ParcelBaseSchema):
	pass


class ParcelResponse(BaseModel):
	parcel_id: int


class ParcelTypeResponse(BaseModel):
	type_id: int
	name: str


class ParcelListResponse(BaseModel):
	parcel_id: int
	name: str
	weight: float
	type_id: int
	type_name: str
	content_value_usd: float
	delivery_price: str | float
	created_at: datetime


class ParcelDetailResponse(BaseModel):
	parcel_id: int
	name: str
	weight: float
	type_id: int
	type_name: str
	content_value_usd: float
	delivery_price: float | Literal['Не рассчитано'] | None
	created_at: datetime
