from datetime import date

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from database.models.chemistry_file import ChemistryFile
from .base import BaseRepo


class ChemistryFileRepo(BaseRepo):
    async def add_or_ignore_file(
            self,
            name: str,
            file_path: str,
            _date: str
    ):
        query = select(ChemistryFile).where(
            ChemistryFile.name == name,
            ChemistryFile.date == _date
        )

        result = await self.session.execute(query)
        existing_file = result.scalar_one_or_none()

        if not existing_file:
            query = insert(ChemistryFile).values(
                name=name,
                file_path=file_path,
                date=_date
            ).returning(ChemistryFile)
            new_file = await self.session.execute(query)
            await self.session.commit()
            return new_file

        return None

    async def get_all_files(self):
        query = select(ChemistryFile)
        result = await self.session.execute(query)
        return result.scalars().all()

