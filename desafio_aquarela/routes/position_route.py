from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from desafio_aquarela.database import get_session
from desafio_aquarela.models import Position

from ..schemas.position_schema import (
    PositionList,
    PositionResponse,
    PositionSchema,
)

router = APIRouter(prefix='/position', tags=['positions'])


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=PositionResponse,
)
def create_position(
    position: PositionSchema, session: Session = Depends(get_session)
):
    """
    Create a new position.

    Args:
        position (PositionSchema): The position data to create.

    Returns:
        PositionResponse: The created position.
    """
    db_position = Position(
        name=position.name,
    )
    session.add(db_position)
    session.commit()
    session.refresh(db_position)
    return db_position


@router.get('/', response_model=PositionList)
def get_position(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    """
    Get all positions.

    Args:
        skip (int, optional): The number of items to skip. Defaults to 0.
        limit (int, optional): The number of items to return. Defaults to 100.

    Returns:
        PositionList: The list of positions.
    """
    positions = session.scalars(
        select(Position).offset(skip).limit(limit)
    ).all()
    return {'position': positions}
