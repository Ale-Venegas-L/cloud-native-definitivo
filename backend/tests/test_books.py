class TestBooks:
    def test_get_books_returns_seeded_catalog(self, client):
        response = client.get("/api/v1/books/")
        assert response.status_code == 200
        # lifespan seed carga 9 libros iniciales
        assert len(response.json()) >= 9

    def test_create_book(self, client, sample_book, as_admin):
        response = client.post("/api/v1/books/", json=sample_book)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_book["title"]
        assert data["author_id"] == sample_book["author_id"]
        assert data["country"] == sample_book["country"]
        assert data["publication_year"] == sample_book["publication_year"]
        assert data["genre"] == sample_book["genre"]
        assert "id" in data

    def test_get_books_with_data(self, client, sample_book, as_admin):
        before = client.get("/api/v1/books/")
        assert before.status_code == 200
        client.post("/api/v1/books/", json=sample_book)
        response = client.get("/api/v1/books/")
        assert response.status_code == 200
        assert len(response.json()) == len(before.json()) + 1

    def test_get_book_by_id(self, client, sample_book, as_admin):
        create_resp = client.post("/api/v1/books/", json=sample_book)
        book_id = create_resp.json()["id"]
        response = client.get(f"/api/v1/books/{book_id}")
        assert response.status_code == 200
        assert response.json()["title"] == sample_book["title"]

    def test_get_book_not_found(self, client):
        response = client.get("/api/v1/books/507f1f77bcf86cd799439011")
        assert response.status_code == 404

    def test_update_book(self, client, sample_book, as_admin):
        create_resp = client.post("/api/v1/books/", json=sample_book)
        book_id = create_resp.json()["id"]
        update_data = {"title": "Cien años de soledad (Edición Anniversary)"}
        response = client.put(f"/api/v1/books/{book_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["title"] == update_data["title"]
        assert response.json()["genre"] == sample_book["genre"]

    def test_update_book_not_found(self, client, as_admin):
        response = client.put("/api/v1/books/507f1f77bcf86cd799439011", json={"title": "Test"})
        assert response.status_code == 404

    def test_delete_book(self, client, sample_book, as_admin):
        create_resp = client.post("/api/v1/books/", json=sample_book)
        book_id = create_resp.json()["id"]
        response = client.delete(f"/api/v1/books/{book_id}")
        assert response.status_code == 204
        get_resp = client.get(f"/api/v1/books/{book_id}")
        assert get_resp.status_code == 404

    def test_delete_book_not_found(self, client, as_admin):
        response = client.delete("/api/v1/books/507f1f77bcf86cd799439011")
        assert response.status_code == 404

    def test_create_book_validation_error(self, client, as_admin):
        response = client.post("/api/v1/books/", json={"title": ""})
        assert response.status_code == 422

    def test_create_book_missing_fields(self, client, as_admin):
        response = client.post("/api/v1/books/", json={"title": "Test"})
        assert response.status_code == 422

    def test_write_without_auth_returns_401(self, client, sample_book):
        response = client.post("/api/v1/books/", json=sample_book)
        assert response.status_code == 401
