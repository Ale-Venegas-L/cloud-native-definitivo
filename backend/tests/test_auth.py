from app.main import app
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import AuthenticatedUser


def test_public_catalog_does_not_require_authentication(client):
    response = client.get("/api/v1/books/")

    assert response.status_code == 200
    assert len(response.json()) == 9


def test_write_without_token_returns_401(client):
    response = client.post(
        "/api/v1/authors/",
        json={
            "name": "Mary Shelley",
            "country": "Inglaterra",
            "birth_year": 1797,
            "death_year": 1851,
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required"


def test_malformed_token_returns_401(client):
    response = client.post(
        "/api/v1/authors/",
        headers={"Authorization": "Bearer not-a-jwt"},
        json={
            "name": "Mary Shelley",
            "country": "Inglaterra",
            "birth_year": 1797,
            "death_year": 1851,
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"


def test_authenticated_non_admin_returns_403(client):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        uid="reader-1",
        email="reader@example.com",
    )

    response = client.post(
        "/api/v1/authors/",
        json={
            "name": "Mary Shelley",
            "country": "Inglaterra",
            "birth_year": 1797,
            "death_year": 1851,
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Administrator role required"


def test_admin_can_create_an_author(client):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        uid="admin-1",
        email="admin@example.com",
        admin=True,
    )

    response = client.post(
        "/api/v1/authors/",
        json={
            "name": "Mary Shelley",
            "country": "Inglaterra",
            "birth_year": 1797,
            "death_year": 1851,
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Mary Shelley"


def test_me_returns_the_authenticated_identity(client):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        uid="admin-1",
        email="admin@example.com",
        admin=True,
        permissions=["books:write"],
    )

    response = client.get("/api/v1/auth/me")

    assert response.status_code == 200
    assert response.json() == {
        "uid": "admin-1",
        "email": "admin@example.com",
        "name": None,
        "picture": None,
        "admin": True,
        "permissions": ["books:write"],
    }
