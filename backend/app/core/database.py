from pymongo import MongoClient
from app.core.config import settings

client: MongoClient = None
db = None


def get_database():
    global client, db
    if db is None:
        client = MongoClient(settings.MONGO_URI)
        db = client[settings.MONGO_DATABASE]
    return db


def close_database():
    global client, db
    if client:
        client.close()
        client = None
        db = None
