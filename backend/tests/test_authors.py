class TestAuthors:
    def test_get_authors_empty(self, client):
        response = client.get("/api/authors/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_author(self, client, sample_author):
        response = client.post("/api/authors/", json=sample_author)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_author["name"]
        assert data["country"] == sample_author["country"]
        assert data["birth_year"] == sample_author["birth_year"]
        assert "id" in data

    def test_get_authors_with_data(self, client, sample_author):
        client.post("/api/authors/", json=sample_author)
        response = client.get("/api/authors/")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_author_by_id(self, client, sample_author):
        create_resp = client.post("/api/authors/", json=sample_author)
        author_id = create_resp.json()["id"]
        response = client.get(f"/api/authors/{author_id}")
        assert response.status_code == 200
        assert response.json()["name"] == sample_author["name"]

    def test_get_author_not_found(self, client):
        response = client.get("/api/authors/507f1f77bcf86cd799439011")
        assert response.status_code == 404

    def test_update_author(self, client, sample_author):
        create_resp = client.post("/api/authors/", json=sample_author)
        author_id = create_resp.json()["id"]
        update_data = {"biography": "Biografía actualizada del autor."}
        response = client.put(f"/api/authors/{author_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["biography"] == update_data["biography"]
        assert response.json()["name"] == sample_author["name"]

    def test_update_author_not_found(self, client):
        response = client.put(
            "/api/authors/507f1f77bcf86cd799439011",
            json={"name": "Test"}
        )
        assert response.status_code == 404

    def test_delete_author(self, client, sample_author):
        create_resp = client.post("/api/authors/", json=sample_author)
        author_id = create_resp.json()["id"]
        response = client.delete(f"/api/authors/{author_id}")
        assert response.status_code == 204
        get_resp = client.get(f"/api/authors/{author_id}")
        assert get_resp.status_code == 404

    def test_delete_author_not_found(self, client):
        response = client.delete("/api/authors/507f1f77bcf86cd799439011")
        assert response.status_code == 404

    def test_get_author_books(self, client, sample_author, sample_book):
        author_resp = client.post("/api/authors/", json=sample_author)
        author_id = author_resp.json()["id"]
        book_data = {**sample_book, "author_id": author_id}
        client.post("/api/books/", json=book_data)
        response = client.get(f"/api/authors/{author_id}/books")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["author_id"] == author_id

    def test_get_author_books_not_found(self, client):
        response = client.get("/api/authors/507f1f77bcf86cd799439011/books")
        assert response.status_code == 404

    def test_create_author_validation_error(self, client):
        response = client.post("/api/authors/", json={"name": ""})
        assert response.status_code == 422

    def test_create_author_missing_fields(self, client):
        response = client.post("/api/authors/", json={"name": "Test"})
        assert response.status_code == 422
