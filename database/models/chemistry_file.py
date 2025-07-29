from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.uuid_pk_mixin import UuidPkMixin


class ChemistryFile(Base, UuidPkMixin):
    __tablename__ = "chemistry_files"

    name: Mapped[str] = mapped_column(unique=True)
    file_path: Mapped[str]
    date: Mapped[str]