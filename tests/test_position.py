from http import HTTPStatus


def test_create_position(client):
    response = client.post(
        '/position/',
        json={
            'name': 'Raphael',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert 'registrationCode' in response.json()


def test_read_position(client):
    response = client.get('/position/')
    assert response.status_code == HTTPStatus.OK

    response_data = response.json()
    assert 'position' in response_data
    positions = response_data['position']

    required_fields = ['name', 'registrationCode']
    for position in positions:
        for field in required_fields:
            assert field in position
