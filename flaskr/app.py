"""Flask app creator file."""
from flask import Flask

from flaskr.routes.adress_data import adress_data_blueprint


def create_app(app_config):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__)

    app.register_blueprint(adress_data_blueprint, url_prefix="/")
    app.config.from_object(f"flaskr.config.{app_config}")
    app.secret_key = "secret string"

    return app