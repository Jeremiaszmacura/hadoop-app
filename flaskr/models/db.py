"""Database instance file."""
from pymongo import MongoClient
from os import environ


client = MongoClient(environ.get("DEV_DATABASE_URI", "localhost:27017"))
db = client.test