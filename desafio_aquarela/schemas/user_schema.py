from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from desafio_aquarela.schemas.position_schema import PositionResponse

from .leader_schema import LeaderResponse


class UserStatus(str, Enum):
    ACTIVE = 'ativo'
    INACTIVE = 'inativo'
    VACATION = 'ferias'


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    name: str
    lastName: str
    positionCode: int
    leaderCode: int
    status: UserStatus
    password: str
    wage: Decimal


class UserSchemaResponse(BaseModel):
    registrationCode: int
    name: str
    lastName: str
    status: UserStatus
    leader: LeaderResponse
    position: PositionResponse

    class Config:
        from_attributes = True


class UserDB(UserSchema):
    registrationCode: int


class UserList(BaseModel):
    users: list[UserSchemaResponse]


class UserSchemaUpdate(BaseModel):
    name: Optional[str] = None
    lastName: Optional[str] = None
    positionCode: Optional[int] = None
    leaderCode: Optional[int] = None
    status: Optional[UserStatus] = None
    password: Optional[str] = None
    wage: Optional[Decimal] = None
