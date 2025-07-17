from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from database.repo.cargo_tracking import CargoTrackingRepo


@dataclass
class RequestsRepo:
    session: AsyncSession

    @property
    def cargo_tracking(self) -> CargoTrackingRepo:
        return CargoTrackingRepo(self.session)


