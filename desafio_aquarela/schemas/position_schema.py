from pydantic import BaseModel


class PositionResponse(BaseModel):
    registrationCode: int
    name: str

    class Config:
        from_attributes = True


class PositionList(BaseModel):
    position: list[PositionResponse]


class PositionSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True
