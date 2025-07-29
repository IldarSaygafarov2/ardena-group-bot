from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from .chemistry_file import ChemistryFileRepo



@dataclass
class RequestsRepo:
    session: AsyncSession


    @property
    def chemistry_file(self) -> ChemistryFileRepo:
        return ChemistryFileRepo(self.session)