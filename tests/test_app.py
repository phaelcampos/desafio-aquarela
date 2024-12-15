from http import HTTPStatus


def test_create_user(client, create_leader_fixture, create_position_fixture):
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
    assert response.status_code == HTTPStatus.CREATED
    assert 'registrationCode' in response.json()


def test_create_user_leader_not_found(client):
    response = client.post(
        '/users',
        json={
            'name': 'Raphael',
            'lastName': 'Campos',
            'positionCode': 1,
            'leaderCode': 0,
            'statusId': 1,
            'password': 'teste123',
            'wage': 3000,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK

    response_data = response.json()
    assert 'users' in response_data
    users = response_data['users']

    # Verifica se cada usuário tem os campos necessários
    required_fields = ['name', 'lastName', 'registrationCode']
    for user in users:
        for field in required_fields:
            assert field in user


def test_update_user(client, create_user_fixture):
    response = client.put(
        f'/users/{create_user_fixture["registrationCode"]}',
        json={'name': 'bob', 'lastName': 'ross'},
    )
    required_fields = ['name', 'lastName', 'registrationCode']
    for field in required_fields:
        assert field in response.json()


def test_update_user_not_found(client):
    response = client.put(
        '/users/0',
        json={
            'name': 'bob',
            'lastName': 'ross',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, create_user_fixture):
    response = client.delete(
        f'/users/{create_user_fixture["registrationCode"]}'
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/9999')

    assert response.status_code == HTTPStatus.NOT_FOUND
