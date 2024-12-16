from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, noload

from desafio_aquarela.database import get_session
from desafio_aquarela.models.user_model import User
from desafio_aquarela.schemas.auth_schema import CustomLoginForm, Token
from desafio_aquarela.service.auth import (
    create_access_token,
    verify_password,
)

# ...
router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: CustomLoginForm = Depends(),
    session: Session = Depends(get_session),
):
    db_user = session.scalar(
        select(User)
        .where(User.registrationCode == form_data.registrationCode)
        .options(noload('*'))
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': int(db_user.registrationCode)})

    return {'access_token': access_token, 'token_type': 'bearer'}
