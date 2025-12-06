def test_register_and_login(client):
    # register
    r = client.post('/auth/register', json={'email': 'u@example.com', 'password': 'secret'})
    assert r.status_code == 200
    data = r.json()
    assert data['email'] == 'u@example.com'

    # login
    r = client.post('/auth/token', data={'username': 'u@example.com', 'password': 'secret'})
    assert r.status_code == 200
    data = r.json()
    assert 'access_token' in data
