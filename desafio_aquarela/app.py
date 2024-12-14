from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from .schemas.user import (
    Message,
    UserDB,
    UserList,
    UserSchema,
    UserSchemaResponse,
    UserSchemaUpdate,
)

app = FastAPI()

database = []


@app.post(
    '/users/',
    status_code=HTTPStatus.CREATED,
    response_model=UserSchemaResponse,
)
def create_user(user: UserSchema):
    user_with_id = UserDB(
        **user.model_dump(), registrationCode=len(database) + 1
    )
    print(user_with_id)
    database.append(user_with_id)

    return user_with_id


@app.get('/users/', response_model=UserList)
def get_user():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserSchemaResponse)
def update_user(user_id: int, user: UserSchemaUpdate):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(**user.model_dump(), registrationCode=user_id)
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted'}
