from dataclasses import asdict

from sqlalchemy import select

from desafio_aquarela.models.userModel import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            name='Raphael',
            lastName='Campos',
            positionCode=1,
            leaderCode=1,
            statusId=1,
            password='teste123',
            wage=3000,
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.name == 'Raphael'))

    assert asdict(user) == {
        'name': 'Raphael',
        'lastName': 'Campos',
        'positionCode': 1,
        'leaderCode': 1,
        'statusId': 1,
        'password': 'teste123',
        'wage': 3000,
        'created_at': time,
    }
