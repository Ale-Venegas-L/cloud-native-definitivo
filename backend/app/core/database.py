from pymongo import MongoClient

from app.core.config import settings

client = None
db = None
_use_mock = False


def get_database():
    global client, db, _use_mock
    if db is None:
        try:
            client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=2000)
            client.server_info()
            db = client[settings.MONGO_DATABASE]
        except Exception:
            import mongomock

            client = mongomock.MongoClient()
            db = client[settings.MONGO_DATABASE]
            _use_mock = True
    return db


def is_mock():
    return _use_mock


def get_client():
    return client


def close_database():
    global client, db
    if client:
        client.close()
        client = None
        db = None
