import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel


class BaseCargoTrackingSchema(BaseModel):
    uni_in_shipment: str
    shipper: str
    destination: Optional[str]
    vehicle_type: str
    date_of_dispatch: date
    current_station: Optional[str]
    remaining_distance: Optional[float]
    number_of_container_or_wagon: str
    arrival_date: Optional[date]
    brand: str
    gross_weight: float
    net_weight: float
    places_number: int


class CargoTrackingCreateSchema(BaseCargoTrackingSchema):
    pass


class CargoTrackingSchema(BaseCargoTrackingSchema):
    id: uuid.UUID


