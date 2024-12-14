from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'name': 'Raphael',
            'lastName': 'Campos',
            'positionCode': 1,
            'leaderCode': 1,
            'statusId': 1,
            'password': 'teste123',
            'wage': 3000,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'name': 'Raphael',
        'lastName': 'Campos',
        'registrationCode': 1,
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'name': 'Raphael',
                'lastName': 'Campos',
                'registrationCode': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'name': 'bob',
            'lastName': 'ross',
            'password': 'mynewpassword',
        },
    )
    print(response.json())
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': 'bob',
        'lastName': 'ross',
        'registrationCode': 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/5',
        json={
            'name': 'bob',
            'lastName': 'ross',
            'password': 'mynewpassword',
        },
    )
    print(response.json())
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/9999')

    assert response.status_code == HTTPStatus.NOT_FOUND
