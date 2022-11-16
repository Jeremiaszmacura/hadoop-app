"""Flask app entry point file."""
from os import environ

from flaskr.app import create_app


app = create_app(environ.get("APP_CONFIG", "DevelopmentConfig"))


if __name__ == "__main__":
    app.run()
