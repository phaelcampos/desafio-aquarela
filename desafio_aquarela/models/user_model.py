from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
    Mapped,
    MappedAsDataclass,
    mapped_column,
    registry,
    relationship,
)

from desafio_aquarela.models.leaders_model import Leader
from desafio_aquarela.models.position_model import Position

from .base import Base

table_registry = registry()


class UserStatus(str, Enum):
    ACTIVE = 'ativo'
    INACTIVE = 'inativo'
    VACATION = 'ferias'


class User(MappedAsDataclass, Base):
    __tablename__ = 'users'
    registrationCode: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    lastName: Mapped[str]
    positionCode: Mapped[int] = mapped_column(
        ForeignKey('position.registrationCode')
    )
    leaderCode: Mapped[int] = mapped_column(
        ForeignKey('leaders.registrationCode')
    )
    status: Mapped[UserStatus] = mapped_column(
        SQLAlchemyEnum(
            UserStatus,
            name='status_enum',
            create_constraint=True,
            native_enum=True,
        )
    )
    password: Mapped[str]
    wage: Mapped[Decimal]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    leader: Mapped['Leader'] = relationship(
        'Leader',
        init=False,
        lazy='joined',
    )
    position: Mapped['Position'] = relationship(
        'Position',
        init=False,
        lazy='joined',
    )
