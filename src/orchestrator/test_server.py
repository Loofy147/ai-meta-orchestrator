import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_hello(client):
    """Test the hello endpoint."""
    rv = client.get("/")
    assert rv.status_code == 200
    assert rv.json == {"message": "Hello from the backend!"}
