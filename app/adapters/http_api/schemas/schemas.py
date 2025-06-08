from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class ParcelTypeBase(BaseModel):
	"""Базовая модель для типа посылки."""
	name: str = Field(..., min_length=1, max_length=50,
	                  description='Название типа посылки')


class ParcelType(ParcelTypeBase):
	"""Тип посылки с ID (используется при работе с БД)."""
	id: int

	model_config = {
		'from_attributes': True,
	}


class ParcelBaseSchema(BaseModel):
	"""Базовая модель данных посылки."""
	name: str = Field(..., min_length=1, max_length=100,
	                  description='Название посылки')
	weight: float = Field(..., gt=0, description='Вес посылки в кг')
	type_id: int = Field(..., gt=0, description='ID типа посылки')
	content_value_usd: float = Field(..., gt=0,
	                                 description='Стоимость содержимого в USD')


class ParcelCreateSchema(ParcelBaseSchema):
	"""Схема для создания новой посылки."""
	pass


class ParcelResponse(BaseModel):
	"""Ответ после создания посылки."""
	parcel_id: int = Field(..., description='ID созданной посылки')


class ParcelTypeResponse(BaseModel):
	"""Схема для отображения типа посылки."""
	type_id: int = Field(..., description='ID типа посылки')
	name: str = Field(..., description='Название типа')


class ParcelListResponse(BaseModel):
	"""Схема ответа при получении списка посылок."""
	parcel_id: int = Field(..., description='ID посылки')
	name: str = Field(..., description='Название посылки')
	weight: float = Field(..., description='Вес посылки в кг')
	type_id: int = Field(..., description='ID типа посылки')
	type_name: str = Field(..., description='Название типа посылки')
	content_value_usd: float = Field(...,
	                                 description='Стоимость содержимого в USD')
	delivery_price: str | float = Field(...,
	                                    description="Цена доставки или 'Не рассчитано'")
	created_at: datetime = Field(..., description='Дата и время создания')


class ParcelDetailResponse(BaseModel):
	"""Схема ответа при получении информации о посылке по ID."""
	parcel_id: int = Field(..., description='ID посылки')
	name: str = Field(..., description='Название посылки')
	weight: float = Field(..., description='Вес посылки в кг')
	type_id: int = Field(..., description='ID типа посылки')
	type_name: str = Field(..., description='Название типа посылки')
	content_value_usd: float = Field(...,
	                                 description='Стоимость содержимого в USD')
	delivery_price: float | Literal['Не рассчитано'] | None = Field(
		..., description="Стоимость доставки или 'Не рассчитано'"
	)
	created_at: datetime = Field(..., description='Дата создания')


class CompanyCreateSchema(BaseModel):
	"""Схема для создания новой транспортной компании."""
	name: str = Field(..., description='Название компании')


class CompanyResponse(CompanyCreateSchema):
	"""Схема ответа при получении данных о компании."""
	id: int = Field(..., description='ID компании')
	name: str = Field(..., description='Название компании')


class BindCompanySchema(BaseModel):
	"""Запрос на привязку посылки к компании."""
	parcel_id: int = Field(..., ge=1, description='ID посылки')
	company_id: int = Field(..., ge=1, description='ID компании')


class BindCompanyResponseSchema(BaseModel):
	"""Ответ на успешную привязку посылки к компании."""
	message: str = Field(default='Компания успешно привязана к посылке',
	                     description='Сообщение об успехе')
