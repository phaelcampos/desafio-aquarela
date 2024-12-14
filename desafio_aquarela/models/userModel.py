from datetime import datetime
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, registry

table_registry = registry()
from .base import Base


class User(MappedAsDataclass, Base):
    __tablename__ = 'users'
    registrationCode: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    lastName: Mapped[str]
    positionCode: Mapped[int]
    leaderCode: Mapped[int]
    statusId: Mapped[int]
    password: Mapped[str]
    wage: Mapped[Decimal]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
