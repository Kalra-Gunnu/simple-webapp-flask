import pytest
from app import app

@pytest.fixture
def client():
    # Create a test client for the Flask app
    app.testing = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test if the homepage returns 200 OK and expected content"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data or b"Hello" in response.data
