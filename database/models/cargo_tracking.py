from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.uuid_pk_mixin import UuidPkMixin


class CargoTracking(Base, UuidPkMixin):
    __tablename__ = "cargo_tracking"

    uni_in_shipment: Mapped[str] = mapped_column(nullable=False)
    shipper: Mapped[str] = mapped_column(nullable=False)
    destination: Mapped[str] = mapped_column(nullable=True)
    vehicle_type: Mapped[str] = mapped_column(nullable=False)
    date_of_dispatch: Mapped[date]
    current_station: Mapped[str] = mapped_column(nullable=True)
    remaining_distance: Mapped[float] = mapped_column(nullable=True, default=0.0)
    number_of_container_or_wagon: Mapped[str] = mapped_column(nullable=False)
    arrival_date: Mapped[date] = mapped_column(nullable=True)
    brand: Mapped[str] = mapped_column(nullable=False)
    gross_weight: Mapped[float]
    net_weight: Mapped[float]
    places_number: Mapped[int]

