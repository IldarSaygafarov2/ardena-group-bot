from typing import Annotated

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, mapped_column

created_at = Annotated[TIMESTAMP, mapped_column(TIMESTAMP, server_default=func.now())]


class Base(DeclarativeBase):
    pass
