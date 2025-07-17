import sqlalchemy as sa

from database.models import CargoTracking
from schemas.cargo_tracking import CargoTrackingCreateSchema
from .base import BaseRepo


class CargoTrackingRepo(BaseRepo):
    async def add_cargo_tracking(
            self,
            cargo_tracking_item: CargoTrackingCreateSchema
    ):
        data = cargo_tracking_item.model_dump()

        stmt = (
            sa.insert(CargoTracking)
            .values(
                **data
            )
            .returning(CargoTracking)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def get_cargo_tracking_by_uni_in_shipment(self, uni_in_shipment: str):
        stmt = (
            sa.select(CargoTracking)
            .where(CargoTracking.uni_in_shipment == uni_in_shipment)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_cargo_tracking(
            self,
            cargo_tracking_item: CargoTrackingCreateSchema,
            uni_in_shipment: str
    ):
        pass