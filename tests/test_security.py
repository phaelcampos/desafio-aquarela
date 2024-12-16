from http import HTTPStatus

from jwt import decode

from desafio_aquarela.service.auth import SECRET_KEY, create_access_token


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert decoded['exp']


def test_get_token(client, create_user_fixture):
    response = client.post(
        '/auth/token',
        params={
            'registrationCode': create_user_fixture['registrationCode'],
            'password': 'teste123',
        },
    )
    token = response.json()
    print(response.json())
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token
