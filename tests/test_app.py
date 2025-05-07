import pytest
from app import app as flask_app

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data  # Adjust based on actual content

def test_error_page(client):
    response = client.get('/non-existent-page')
    assert response.status_code == 404
    assert b'Error' in response.data  # Adjust based on actual content