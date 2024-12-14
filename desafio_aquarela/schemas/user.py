from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    name: str
    lastName: str
    positionCode: int
    leaderCode: int
    statusId: int
    password: str
    wage: Decimal


class UserSchemaResponse(BaseModel):
    registrationCode: int
    name: str
    lastName: str


class UserDB(UserSchema):
    registrationCode: int


class UserList(BaseModel):
    users: list[UserSchemaResponse]


class UserSchemaUpdate(BaseModel):
    name: Optional[str] = None
    lastName: Optional[str] = None
    positionCode: Optional[int] = 0
    leaderCode: Optional[int] = 0
    statusId: Optional[int] = 0
    password: Optional[str] = None
    wage: Optional[Decimal] = 0
