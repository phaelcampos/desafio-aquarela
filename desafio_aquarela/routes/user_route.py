from decimal import Decimal
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from desafio_aquarela.database import get_session
from desafio_aquarela.models import User
from desafio_aquarela.service.auth import get_current_user, get_password_hash
from desafio_aquarela.service.validator import EntityValidator

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
async def create_user(
    user: UserSchema, session: Session = Depends(get_session)
):
    validator = EntityValidator(session)

    if user.leaderCode is not None:
        if not await validator.validate_leader(user.leaderCode):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Leader not found'
            )
    if user.positionCode is not None:
        if not await validator.validate_position(user.positionCode):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Position not found',
            )

    db_user = User(
        name=user.name,
        lastName=user.lastName,
        positionCode=user.positionCode,
        leaderCode=user.leaderCode,
        status=user.status,
        password=get_password_hash(user.password),
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
async def update_user(
    registration_code: int,
    user: UserSchemaUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.registrationCode != registration_code:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    validator = EntityValidator(session)
    if user.leaderCode is not None:
        if not await validator.validate_leader(user.leaderCode):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Leader not found'
            )
    if user.positionCode is not None:
        if not await validator.validate_position(user.positionCode):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Position not found',
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
            if field == 'password':
                value = get_password_hash(value)  # noqa
            setattr(db_user, field, value)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete('/{registration_code}', response_model=Message)
def delete_user(
    registration_code: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),

):
    if current_user.registrationCode != registration_code:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
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
