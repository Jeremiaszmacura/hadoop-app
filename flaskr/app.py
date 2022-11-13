"""Flask app creator file."""
from flask import Flask

from flaskr.routes.users import users_blueprint
from flaskr.models.db import db


def create_app(app_config):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__)

    app.register_blueprint(users_blueprint, url_prefix="/")

    app.config.from_object(f"flaskr.config.{app_config}")
    print(app_config)

    app.secret_key = "secret string"

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app