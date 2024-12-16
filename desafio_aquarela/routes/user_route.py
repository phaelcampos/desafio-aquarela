from decimal import Decimal
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from desafio_aquarela.database import get_session
from desafio_aquarela.models import User
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
    """
    Create a new user in the system.

    Args:
        user (UserSchema): The information of the user to create.
        session (Session, optional): The database session dependency.

    Returns:
        UserSchemaResponse: The created user's information.

    Raises:
        HTTPException: If the leader or position associated with the user
        is not found.
    """

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
    """
    Return a list of all users.

    Args:
        skip (int, optional): The number of records to skip. Defaults to 0.
        limit (int, optional): The number of records to limit the query to.
        Defaults to 100.
        session (Session, optional): The database session dependency.
        Defaults to Depends(get_session).

    Returns:
        UserList: A dictionary containing the list of users,
        each represented as a UserSchemaResponse object.
    """
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
):
    """
    Update an existing user's information by registration code.

    Args:
        registration_code (int): The unique code identifying
        the user to update.
        user (UserSchemaUpdate): The updated user information.
        session (Session): The database session dependency.

    Returns:
        UserSchemaResponse: The updated user information.
    """

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
            setattr(db_user, field, value)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete('/{registration_code}', response_model=Message)
def delete_user(
    registration_code: int, session: Session = Depends(get_session)
):
    """
    Delete a user from the system.

    Args:
        registration_code (int): The registration code of the user to delete.
        session (Session, optional): The database session dependency.

    Returns:
        Message: A message indicating that the user was deleted.

    Raises:
        HTTPException: If the user is not found.
    """

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
