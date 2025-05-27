from app.adapters.database.tables import parcel_types, parcels

from sqlalchemy.orm import relationship, registry

from app.applications.dataclasses.dataclasses import Parcel, ParcelType

mapper_registry = registry()

mapper_registry.map_imperatively(
    Parcel,
    parcels,
    properties={
        'type': relationship(ParcelType, backref='parcels')
    }
)
mapper_registry.map_imperatively(ParcelType, parcel_types)