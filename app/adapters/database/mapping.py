from sqlalchemy.orm import relationship, registry

from app.adapters.database.tables import company, parcels, parcel_types
from app.applications.dataclasses.dataclasses import Parcel, ParcelType, Company

mapper_registry = registry()

mapper_registry.map_imperatively(
    Parcel,
    parcels,
    properties={
        'type': relationship(ParcelType, backref='parcels'),
        'company': relationship(Company, backref='parcels'),
    }
)
mapper_registry.map_imperatively(ParcelType, parcel_types)
mapper_registry.map_imperatively(Company, company)
