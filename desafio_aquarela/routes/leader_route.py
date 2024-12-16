from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from desafio_aquarela.database import get_session
from desafio_aquarela.models import Leader
from desafio_aquarela.models.user_model import User

from ..schemas.leader_schema import (
    LeaderList,
    LeaderResponse,
    LeaderSchema,
    Message,
)

router = APIRouter(prefix='/leader', tags=['leaders'])


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=LeaderResponse,
)
def create_leader(
    leader: LeaderSchema, session: Session = Depends(get_session)
):
    """
    Create a new leader.

    Args:
        leader (LeaderSchema): The leader data to create.

    Returns:
        LeaderResponse: The created leader.

    Raises:
        HTTPException: If the leader already exists.
    """

    db_leader = Leader(
        name=leader.name,
    )
    session.add(db_leader)
    session.commit()
    session.refresh(db_leader)
    return db_leader


@router.get('/', response_model=LeaderList)
def get_leader(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    """
    Return a list of leaders.

    Args:
        skip (int, optional): The number of records to skip. Defaults to 0.
        limit (int, optional): The number of records to limit the query to.
        Defaults to 100.
        session (Session, optional): The database session dependency.
        Defaults to Depends(get_session).

    Returns:
        LeaderList: A dictionary containing the list of leaders,
        each represented as a LeaderSchemaResponse object.
    """
    leaders = session.scalars(select(Leader).offset(skip).limit(limit)).all()
    return {'leader': leaders}


@router.put('/{registration_code}', response_model=LeaderResponse)
def update_leader(
    registration_code: int,
    leader: LeaderSchema,
    session: Session = Depends(get_session),
):
    """
    Update a leader by registration code.

    Args:
        registration_code (int): The registration code of the leader to update.
        leader (LeaderSchema): The updated leader information.
        session (Session): The database session dependency.

    Returns:
        LeaderResponse: The updated leader information.

    Raises:
        HTTPException: If the leader is not found.
    """
    db_leader = session.scalar(
        select(Leader).where(Leader.registrationCode == registration_code)
    )
    if not db_leader:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Leader not found'
        )

    db_leader.name = leader.name
    session.commit()
    session.refresh(db_leader)
    return db_leader


@router.delete('/{registration_code}', response_model=Message)
def delete_leader(
    registration_code: int, session: Session = Depends(get_session)
):
    """
    Delete a leader from the system.

    Args:
        registration_code (int): The registration code of the leader to delete.
        session (Session, optional): The database session dependency.

    Returns:
        Message: A message indicating that the leader was deleted.

    Raises:
        HTTPException: If the leader is not found.
    """
    db_user = session.scalar(
        select(User).where(User.leaderCode == registration_code)
    )
    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Leader is associated with a user',
        )

    db_leader = session.scalar(
        select(Leader).where(Leader.registrationCode == registration_code)
    )
    if not db_leader:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Leader not found'
        )
    session.delete(db_leader)
    session.commit()
    return {'message': 'Leader deleted'}
