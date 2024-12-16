from fastapi import Form
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class Message(BaseModel):
    message: str


class CustomLoginForm(BaseModel):
    registrationCode: int
    password: str

    @classmethod
    def as_form(
        cls,
        registrationCode: str = Form(...),
        password: str = Form(...),
    ):
        return cls(registrationCode=registrationCode, password=password)


class TokenData(BaseModel):
    username: str | None = None
