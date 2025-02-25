from app import app
import pytest

def test_home():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200