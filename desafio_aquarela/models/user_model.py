from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
    Mapped,
    MappedAsDataclass,
    mapped_column,
    registry,
    relationship,
)

from desafio_aquarela.models.leaders_model import Leader

from .base import Base

table_registry = registry()


class User(MappedAsDataclass, Base):
    __tablename__ = 'users'
    registrationCode: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    lastName: Mapped[str]
    positionCode: Mapped[int]
    leaderCode: Mapped[int] = mapped_column(
        ForeignKey('leaders.registrationCode')
    )
    statusId: Mapped[int]
    password: Mapped[str]
    wage: Mapped[Decimal]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    leader: Mapped['Leader'] = relationship(
        'Leader',
        init=False,
        lazy='joined',  # para carregar automaticamente
    )
