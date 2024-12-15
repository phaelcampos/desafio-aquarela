from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, registry

from .base import Base

table_registry = registry()


class Position(MappedAsDataclass, Base):
    __tablename__ = 'position'
    registrationCode: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
