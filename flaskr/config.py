"""App configuration file."""
from os import environ, path
from dotenv import load_dotenv


basedir: str = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, "../.env"))


class Config:  # pylint: disable=too-few-public-methods
    """Base config."""

    TESTING: bool = False
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False


class ProductionConfig(Config):  # pylint: disable=too-few-public-methods
    """Uses production PostgreSQL database container."""

    ENV: str = "production"


class DevelopmentConfig(Config):  # pylint: disable=too-few-public-methods
    """Uses PostgreSQL in docker container."""

    # SQLALCHEMY_DATABASE_URI = environ.get("DEV_DATABASE_URI")
    ENV: str = "development"
    DEBUG: bool = True
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True
    MONGO_URI: str = environ.get("DEV_DATABASE_URI", "localhost:27017")
    TEMPLATES_AUTO_RELOAD: bool = True


class TestingConfig(Config):  # pylint: disable=too-few-public-methods
    """Uses sqlite in memory."""

    ENV: str = "development"
    MONGO_URI: str = environ.get("DEV_DATABASE_URI", "localhost:27017")
    CRYPTO_KEY: str = environ.get("CRYPTO_KEY")
    TESTING: bool = True
