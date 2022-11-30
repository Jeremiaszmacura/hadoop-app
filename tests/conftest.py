"""Config tests."""
import pytest

from flaskr.app import create_app


@pytest.fixture()
def app():
    """Prepare app instance for testing purpose."""
    app = create_app("TestingConfig")  # pylint: disable=redefined-outer-name

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):  # pylint: disable=redefined-outer-name
    """Creates a test client for app."""
    return app.test_client()


@pytest.fixture()
def runner(app):  # pylint: disable=redefined-outer-name
    """create a FlaskCliRunner, which runs CLI commands in isolation."""
    return app.test_cli_runner()
