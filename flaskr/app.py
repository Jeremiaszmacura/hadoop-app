"""Flask app creator file."""
from flask import Flask

from flaskr.routes.address_data import address_data_blueprint


def create_app(app_config: str):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__)

    app.register_blueprint(address_data_blueprint, url_prefix="/")
    app.config.from_object(f"flaskr.config.{app_config}")
    app.secret_key = "secret string"

    return app