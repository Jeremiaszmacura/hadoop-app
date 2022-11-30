"""Database instance file."""
from os import environ

from pymongo import MongoClient
from cryptography.fernet import Fernet


client = MongoClient(environ.get("DEV_DATABASE_URI", "localhost:27017"))
db = client.test

client_backup = MongoClient(environ.get("BACKUP_DATABASE_URI2", "localhost:27017"))
db_backup = client_backup.test

key = environ.get("CRYPTO_KEY", Fernet.generate_key())
if isinstance(key, str):
    key = bytes(key, "utf-8")
fernet = Fernet(key)
