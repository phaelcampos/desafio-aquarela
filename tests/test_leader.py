from http import HTTPStatus


def test_create_leader(client):
    response = client.post(
        '/leader/',
        json={
            'name': 'Raphael',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert 'registrationCode' in response.json()


def test_read_leader(client):
    response = client.get('/leader/')
    assert response.status_code == HTTPStatus.OK

    response_data = response.json()
    assert 'leader' in response_data
    leaders = response_data['leader']

    required_fields = ['name', 'registrationCode']
    for leader in leaders:
        for field in required_fields:
            assert field in leader


def test_update_leader(client):
    create_response = client.post(
        '/leader/',
        json={
            'name': 'Raphael',
        },
    )
    response = client.put(
        f'/leader/{create_response.json()["registrationCode"]}',
        json={'name': 'bob'},
    )
    required_fields = ['name', 'registrationCode']
    for field in required_fields:
        assert field in response.json()


def test_update_leader_not_found(client):
    response = client.put(
        '/users/3332323',
        json={
            'name': 'bob',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_leader(client):
    create_response = client.post(
        '/leader/',
        json={
            'name': 'Raphael',
        },
    )
    response = client.delete(
        f'/leader/{create_response.json()["registrationCode"]}'
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Leader deleted'}


def test_delete_leader_not_found(client):
    response = client.delete('/leader/9999')

    assert response.status_code == HTTPStatus.NOT_FOUND
