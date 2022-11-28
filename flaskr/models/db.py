"""Database instance file."""
from pymongo import MongoClient
from cryptography.fernet import Fernet
from os import environ


client = MongoClient(environ.get("DEV_DATABASE_URI", "localhost:27017"))
db = client.test

key = bytes(environ.get("CRYPTO_KEY", Fernet.generate_key()), "utf-8")
fernet = Fernet(key)
