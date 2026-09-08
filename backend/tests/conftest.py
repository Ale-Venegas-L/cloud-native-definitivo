import pytest
from fastapi.testclient import TestClient

from app.core import database
from app.main import app
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import AuthenticatedUser


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client
    database.close_database()


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def admin_user() -> AuthenticatedUser:
    return AuthenticatedUser(uid="admin-1", email="admin@example.com", admin=True)


@pytest.fixture
def as_admin(admin_user):
    app.dependency_overrides[get_current_user] = lambda: admin_user
    return admin_user


@pytest.fixture
def sample_author() -> dict:
    return {
        "name": "Jorge Luis Borges",
        "country": "Argentina",
        "birth_year": 1899,
        "death_year": 1986,
        "biography": "Escritor y ensayista argentino.",
        "image_url": "/authors/borges.webp",
    }


@pytest.fixture
def sample_book() -> dict:
    return {
        "title": "Ficciones",
        "author_id": "507f1f77bcf86cd799439011",
        "country": "Argentina",
        "publication_year": 1944,
        "genre": "Cuentos",
        "description": "Colección de cuentos fantásticos.",
        "cover_url": "/covers/ficciones.webp",
    }
