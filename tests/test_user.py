"""File containing tests for User database model."""

def test_request_example(client):
    """Test."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Scraping Words Tool" in response.data
