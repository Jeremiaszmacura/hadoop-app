"""Flask app entry point file."""
from os import environ

from flask import Flask

from flaskr.app import create_app


app: Flask = create_app(environ.get("APP_CONFIG", "DevelopmentConfig"))


if __name__ == "__main__":
    app.run()
