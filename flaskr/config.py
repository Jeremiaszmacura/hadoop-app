"""App configuration file."""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, "../.env"))


class Config(object):
    """Base config."""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Uses production PostgreSQL database container."""

    SQLALCHEMY_DATABASE_URI = environ.get("PROD_DATABASE_URI")


class DevelopmentConfig(Config):
    """Uses PostgreSQL in docker container."""

    SQLALCHEMY_DATABASE_URI = environ.get("DEV_DATABASE_URI")


class TestingConfig(Config):
    """Uses sqlite in memory."""

    SQLALCHEMY_DATABASE_URI = environ.get("TEST_DATABASE_URI")
    TESTING = True