from decimal import Decimal
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from desafio_aquarela.database import get_session
from desafio_aquarela.models import Leader, User

from ..schemas.user_schema import (
    Message,
    UserList,
    UserSchema,
    UserSchemaResponse,
    UserSchemaUpdate,
)

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=UserSchemaResponse,
)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_leader = session.scalar(
        select(Leader).where(Leader.registrationCode == user.leaderCode)
    )
    if not db_leader:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Leader not found'
        )
    db_user = User(
        name=user.name,
        lastName=user.lastName,
        positionCode=user.positionCode,
        leaderCode=user.leaderCode,
        statusId=user.statusId,
        password=user.password,
        wage=user.wage,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get('/', response_model=UserList)
def get_user(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(
        select(User)
        .options(joinedload(User.leader))  # Carrega o leader junto
        .offset(skip)
        .limit(limit)
    ).all()
    return {'users': users}


@router.put('/{registration_code}', response_model=UserSchemaResponse)
def update_user(
    registration_code: int,
    user: UserSchemaUpdate,
    session: Session = Depends(get_session),
):
    if user.leaderCode is not None:
        db_leader = session.scalar(
            select(Leader).where(Leader.registrationCode == user.leaderCode)
        )
        if not db_leader:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Leader not found'
            )
    db_user = session.scalar(
        select(User).where(User.registrationCode == registration_code)
    )
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    user_data = user.model_dump(exclude_unset=True)

    for field, value in user_data.items():
        if value is not None and (
            not isinstance(value, (int, Decimal)) or value != 0
        ):
            setattr(db_user, field, value)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete('/{registration_code}', response_model=Message)
def delete_user(
    registration_code: int, session: Session = Depends(get_session)
):
    db_user = session.scalar(
        select(User).where(User.registrationCode == registration_code)
    )
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    session.delete(db_user)
    session.commit()
    return {'message': 'User deleted'}
