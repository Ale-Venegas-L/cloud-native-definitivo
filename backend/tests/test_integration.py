import mongomock
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def mock_db():
    client = mongomock.MongoClient()
    db = client["classic_library_integration"]
    yield db
    client.close()


@pytest.fixture(scope="function")
def client(mock_db):
    import app.core.database as db_module

    db_module.db = mock_db
    db_module.client = mock_db.client
    db_module._use_mock = True

    from app.main import app
    from app.modules.auth.dependencies import get_current_user
    from app.modules.auth.schemas import AuthenticatedUser

    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        uid="admin-1", email="admin@example.com", admin=True
    )

    with TestClient(app) as c:
        mock_db.authors.delete_many({})
        mock_db.books.delete_many({})
        yield c

    app.dependency_overrides.clear()
    db_module.db = None
    db_module.client = None
    db_module._use_mock = False


@pytest.fixture
def author_data():
    return {
        "name": "Gabriel García Márquez",
        "country": "Colombia",
        "birth_year": 1927,
        "death_year": 2014,
        "biography": "Escritor y periodista colombiano.",
        "image_url": "/authors/garcia-marquez.webp",
    }


@pytest.fixture
def book_data():
    return {
        "title": "Cien años de soledad",
        "author_id": "507f1f77bcf86cd799439011",
        "country": "Colombia",
        "publication_year": 1967,
        "genre": "Novela",
        "description": "Obra maestra del realismo mágico.",
        "cover_url": "/covers/cien-anos.webp",
    }


class TestHealthIntegration:
    def test_health_returns_ok(self, client):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["mock_db"] is True

    def test_health_indicates_mock(self, client):
        response = client.get("/api/v1/health")
        assert response.json()["mock_db"] is True


class TestAuthorsCRUDIntegration:
    def test_full_author_lifecycle(self, client, author_data):
        create_resp = client.post("/api/v1/authors/", json=author_data)
        assert create_resp.status_code == 201
        author_id = create_resp.json()["id"]

        get_resp = client.get(f"/api/v1/authors/{author_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["name"] == author_data["name"]

        list_resp = client.get("/api/v1/authors/")
        assert list_resp.status_code == 200
        assert len(list_resp.json()) == 1

        update_data = {"biography": "Biografía actualizada."}
        update_resp = client.put(f"/api/v1/authors/{author_id}", json=update_data)
        assert update_resp.status_code == 200
        assert update_resp.json()["biography"] == "Biografía actualizada."

        delete_resp = client.delete(f"/api/v1/authors/{author_id}")
        assert delete_resp.status_code == 204

        get_deleted = client.get(f"/api/v1/authors/{author_id}")
        assert get_deleted.status_code == 404

    def test_create_multiple_authors(self, client, author_data):
        for i in range(3):
            data = {**author_data, "name": f"Autor {i}"}
            resp = client.post("/api/v1/authors/", json=data)
            assert resp.status_code == 201

        list_resp = client.get("/api/v1/authors/")
        assert len(list_resp.json()) == 3

    def test_author_not_found_returns_404(self, client):
        resp = client.get("/api/v1/authors/507f1f77bcf86cd799439011")
        assert resp.status_code == 404

    def test_create_author_invalid_data(self, client):
        resp = client.post("/api/v1/authors/", json={"name": ""})
        assert resp.status_code == 422

    def test_create_author_missing_required(self, client):
        resp = client.post("/api/v1/authors/", json={"name": "Test"})
        assert resp.status_code == 422


class TestBooksCRUDIntegration:
    def test_full_book_lifecycle(self, client, book_data):
        create_resp = client.post("/api/v1/books/", json=book_data)
        assert create_resp.status_code == 201
        book_id = create_resp.json()["id"]

        get_resp = client.get(f"/api/v1/books/{book_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["title"] == book_data["title"]

        list_resp = client.get("/api/v1/books/")
        assert list_resp.status_code == 200
        assert len(list_resp.json()) == 1

        update_data = {"title": "Cien años de soledad (Edición Anniversary)"}
        update_resp = client.put(f"/api/v1/books/{book_id}", json=update_data)
        assert update_resp.status_code == 200
        assert "Anniversary" in update_resp.json()["title"]

        delete_resp = client.delete(f"/api/v1/books/{book_id}")
        assert delete_resp.status_code == 204

        get_deleted = client.get(f"/api/v1/books/{book_id}")
        assert get_deleted.status_code == 404

    def test_create_multiple_books(self, client, book_data):
        for i in range(5):
            data = {**book_data, "title": f"Libro {i}"}
            resp = client.post("/api/v1/books/", json=data)
            assert resp.status_code == 201

        list_resp = client.get("/api/v1/books/")
        assert len(list_resp.json()) == 5

    def test_book_not_found_returns_404(self, client):
        resp = client.get("/api/v1/books/507f1f77bcf86cd799439011")
        assert resp.status_code == 404

    def test_create_book_invalid_data(self, client):
        resp = client.post("/api/v1/books/", json={"title": ""})
        assert resp.status_code == 422

    def test_update_nonexistent_book(self, client):
        resp = client.put("/api/v1/books/507f1f77bcf86cd799439011", json={"title": "Test"})
        assert resp.status_code == 404

    def test_delete_nonexistent_book(self, client):
        resp = client.delete("/api/v1/books/507f1f77bcf86cd799439011")
        assert resp.status_code == 404


class TestAuthorBooksIntegration:
    def test_get_books_by_author(self, client, author_data, book_data):
        author_resp = client.post("/api/v1/authors/", json=author_data)
        author_id = author_resp.json()["id"]

        book1 = {**book_data, "author_id": author_id, "title": "Libro 1"}
        book2 = {**book_data, "author_id": author_id, "title": "Libro 2"}
        client.post("/api/v1/books/", json=book1)
        client.post("/api/v1/books/", json=book2)

        resp = client.get(f"/api/v1/authors/{author_id}/books")
        assert resp.status_code == 200
        assert len(resp.json()) == 2
        assert all(b["author_id"] == author_id for b in resp.json())

    def test_get_books_by_nonexistent_author(self, client):
        resp = client.get("/api/v1/authors/507f1f77bcf86cd799439011/books")
        assert resp.status_code == 404


class TestCORSIntegration:
    def test_cors_allows_frontend_origin(self, client):
        resp = client.options(
            "/api/v1/health",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert resp.status_code == 200
