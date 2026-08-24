import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import mongomock


@pytest.fixture(scope="function")
def mock_db():
    client = mongomock.MongoClient()
    db = client["classic_library_test"]
    yield db
    client.close()


@pytest.fixture(scope="function")
def client(mock_db):
    import app.core.database as db_module
    db_module.db = mock_db
    db_module.client = mock_db.client
    db_module._use_mock = True

    with TestClient(app_main()) as c:
        mock_db.authors.delete_many({})
        mock_db.books.delete_many({})
        yield c

    db_module.db = None
    db_module.client = None
    db_module._use_mock = False


@pytest.fixture
def sample_author():
    return {
        "name": "Gabriel García Márquez",
        "country": "Colombia",
        "birth_year": 1927,
        "death_year": 2014,
        "biography": "Escritor y periodista colombiano, premio Nobel de Literatura 1982.",
        "image_url": "/authors/garcia-marquez.webp"
    }


@pytest.fixture
def sample_book():
    return {
        "title": "Cien años de soledad",
        "author_id": "507f1f77bcf86cd799439011",
        "country": "Colombia",
        "publication_year": 1967,
        "genre": "Novela",
        "description": "Obra maestra del realismo mágico.",
        "cover_url": "/covers/cien-anos.webp"
    }


def app_main():
    from app.main import app
    return app
