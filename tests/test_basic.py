from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_root():
    r = client.get('/')
    assert r.status_code == 200
    assert r.json().get('message') == 'Personal Finance Tracker API'


def test_docs_available():
    r = client.get('/docs')
    assert r.status_code == 200
