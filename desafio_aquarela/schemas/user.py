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
    positionCode: Optional[int] = None
    leaderCode: Optional[int] = None
    statusId: Optional[int] = None
    password: Optional[str] = None
    wage: Optional[Decimal] = None
