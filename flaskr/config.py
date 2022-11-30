"""App configuration file."""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, "../.env"))


class Config:  # pylint: disable=too-few-public-methods
    """Base config."""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):  # pylint: disable=too-few-public-methods
    """Uses production PostgreSQL database container."""

    ENV = "production"


class DevelopmentConfig(Config):  # pylint: disable=too-few-public-methods
    """Uses PostgreSQL in docker container."""

    # SQLALCHEMY_DATABASE_URI = environ.get("DEV_DATABASE_URI")
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MONGO_URI = environ.get("DEV_DATABASE_URI", "localhost:27017")
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):  # pylint: disable=too-few-public-methods
    """Uses sqlite in memory."""

    ENV = "development"
    MONGO_URI = environ.get("DEV_DATABASE_URI", "localhost:27017")
    CRYPTO_KEY = environ.get("CRYPTO_KEY")
    TESTING = True
