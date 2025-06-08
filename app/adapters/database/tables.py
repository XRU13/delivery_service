from sqlalchemy import (
	Column,
	Integer,
	String,
	Float,
	ForeignKey,
	DateTime,
	Boolean,
	MetaData,
	Table,
)
from datetime import datetime

metadata = MetaData()

parcel_types = Table(
	'parcel_types',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(50), unique=True, nullable=False),
)

parcels = Table(
	'parcels',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(50), nullable=False),
	Column('weight', Float, nullable=False),
	Column('type_id', Integer, ForeignKey('parcel_types.id'), nullable=False),
	Column('content_value_usd', Float, nullable=False),
	Column('delivery_price', Float, nullable=True),
	Column('session_id', String(100), nullable=False, index=True),
	Column('created_at', DateTime, default=datetime.now()),
	Column('is_processed', Boolean, default=False),
	Column('company_id', Integer, ForeignKey('company.id'), nullable=True),
)

company = Table(
	'company',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(50), nullable=False),
)
