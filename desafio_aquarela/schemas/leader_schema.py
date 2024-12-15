from pydantic import BaseModel


class Message(BaseModel):
    message: str


class LeaderResponse(BaseModel):
    registrationCode: int
    name: str

    class Config:
        from_attributes = True


class LeaderList(BaseModel):
    leader: list[LeaderResponse]


class LeaderSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True
