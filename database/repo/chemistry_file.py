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
            file_type: str,
            _date: str
    ):
        # Ищем файл только по имени, без учета даты
        query = select(ChemistryFile).where(
            ChemistryFile.name == name
        )

        result = await self.session.execute(query)
        existing_file = result.scalar_one_or_none()

        if not existing_file:
            # Если файл не существует, создаем новый
            query = insert(ChemistryFile).values(
                name=name,
                file_path=file_path,
                file_type=file_type,
                date=_date
            ).returning(ChemistryFile)
            new_file = await self.session.execute(query)
            await self.session.commit()
            return new_file.scalar_one()
        else:
            # Если файл существует, обновляем его данные
            existing_file.file_path = file_path
            existing_file.date = _date
            existing_file.file_type = file_type
            await self.session.commit()
            return existing_file

    async def get_all_files(self):
        query = select(ChemistryFile)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_file_by_type(self, file_type: str):
        query = select(ChemistryFile).where(
            ChemistryFile.file_type == file_type
        )
        result = await self.session.execute(query)
        return result.scalars().all()


