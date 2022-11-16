"""Config tests."""
import pytest
from flaskr.app import create_app


@pytest.fixture()
def app():
    """Prepare app instance for testing purpose."""
    app = create_app("TestingConfig")

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    """Creates a test client for app."""
    return app.test_client()


@pytest.fixture()
def runner(app):
    """create a FlaskCliRunner, which runs CLI commands in isolation."""
    return app.test_cli_runner()