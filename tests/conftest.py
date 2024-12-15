from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from desafio_aquarela.app import app
from desafio_aquarela.database import get_session
from desafio_aquarela.models.user_model import table_registry
from desafio_aquarela.settings import Settings


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(Settings().DATABASE_URL)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)

    yield time

    event.remove(model, 'before_insert', fake_time_handler)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def create_user_fixture(
    client, create_leader_fixture, create_position_fixture
):
    response = client.post(
        '/users',
        json={
            'name': 'Raphael',
            'lastName': 'Campos',
            'positionCode': create_position_fixture['registrationCode'],
            'leaderCode': create_leader_fixture['registrationCode'],
            'statusId': 1,
            'password': 'teste123',
            'wage': 3000,
        },
    )
    user_data = response.json()
    return user_data


@pytest.fixture
def create_leader_fixture(client):
    response = client.post(
        '/leader',
        json={
            'name': 'Lider',
        },
    )
    leader_data = response.json()
    return leader_data


@pytest.fixture
def create_position_fixture(client):
    response = client.post(
        '/position',
        json={
            'name': 'Posição',
        },
    )
    position_data = response.json()
    return position_data
