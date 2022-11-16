"""File containing tests for User database model."""
from tests.consts import BOOK_MODEL_POST_JSON


def test_request_example(client):
    """Test."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, World!" in response.data


def test_book_model_get(client):
    """Test GET /users route - getting all uesrs from database."""
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_book_model_post(client):
    """Test POST /users route - adding new user to database."""
    response = client.post("/users", json=BOOK_MODEL_POST_JSON)
    assert response.status_code == 200
    assert (
        f'User with name: {BOOK_MODEL_POST_JSON["name"]} and surname {BOOK_MODEL_POST_JSON["surname"]} successfully added'
        in str(response.data)
    )