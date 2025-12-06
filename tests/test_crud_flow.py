def auth_header(client):
    r = client.post('/auth/register', json={'email': 'a@example.com', 'password': 'pw'})
    assert r.status_code == 200
    r = client.post('/auth/token', data={'username': 'a@example.com', 'password': 'pw'})
    token = r.json()['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_categories_and_transactions(client):
    headers = auth_header(client)
    # create category
    r = client.post('/categories/', json={'name': 'Food'}, headers=headers)
    assert r.status_code == 200
    cat = r.json()
    assert cat['name'] == 'Food'

    # create transaction
    tx_payload = {'amount': 12.5, 'date': '2023-12-01', 'description': 'Lunch', 'category_id': cat['id']}
    r = client.post('/transactions/', json=tx_payload, headers=headers)
    assert r.status_code == 200
    tx = r.json()
    assert tx['amount'] == 12.5

    # list transactions
    r = client.get('/transactions/', headers=headers)
    assert r.status_code == 200
    arr = r.json()
    assert any(t['id'] == tx['id'] for t in arr)
