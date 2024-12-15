from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from desafio_aquarela.database import get_session
from desafio_aquarela.models import Leader

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
    leaders = session.scalars(select(Leader).offset(skip).limit(limit)).all()
    return {'leader': leaders}


@router.put('/{registration_code}', response_model=LeaderResponse)
def update_leader(
    registration_code: int,
    leader: LeaderSchema,
    session: Session = Depends(get_session),
):
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
