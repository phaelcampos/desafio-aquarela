from sqlalchemy import select
from sqlalchemy.orm import Session

from desafio_aquarela.models.position_model import Position

from ..models import Leader, User


class EntityValidator:
    def __init__(self, session: Session):
        self.session = session

    async def validate_leader(self, leader_code: int) -> Leader:
        db_leader = self.session.scalar(
            select(Leader).where(Leader.registrationCode == leader_code)
        )
        if not db_leader:
            return False
        return True

    async def validate_position(self, registration_code: int) -> User:
        db_user = self.session.scalar(
            select(Position).where(
                Position.registrationCode == registration_code
            )
        )
        if not db_user:
            return False
        return True
