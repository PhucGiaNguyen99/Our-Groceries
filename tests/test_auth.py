import json
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_register_success(client):
    response = client.post('/register', json={
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secure123'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully'

def test_register_missing_fields(client):
    response = client.post('/register', json={
        'username': 'bob'
    })
    assert response.status_code == 400
    assert 'Missing fields' in response.get_json()['error']

def test_register_duplicate_user(client):
    client.post('/register', json={
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secure123'
    })
    response = client.post('/register', json={
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secure123'
    })
    assert response.status_code == 400
    assert 'User already exists' in response.get_json()['error']

def test_login_success(client):
    client.post('/register', json={
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secure123'
    })
    response = client.post('/login', json={
        'username': 'alice',
        'password': 'secure123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_login_invalid_credentials(client):
    response = client.post('/login', json={
        'username': 'notexist',
        'password': 'wrong'
    })
    assert response.status_code == 401
    assert 'Invalid credentials' in response.get_json()['error']
