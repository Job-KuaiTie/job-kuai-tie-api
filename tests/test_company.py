class TestCompany:
    def test_create_company(self, client, default_account):
        url = "https://thisisacoolcompany.com"
        size = 20
        owner_id = default_account

        response = client.post(
            "/companies/", json={"url": url, "size": size, "owner_id": owner_id}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["url"] == url
        assert data["size"] == size
        assert data["owner_id"] == owner_id
        assert "id" in data

    def test_read_companies(self, client):
        response = client.get("/companies/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_read_company(self, client, default_company):
        # Arrange: Get the company id
        company_id = default_company.id

        # Act: Read it back
        response = client.get(f"/companies/{company_id}")

        # Assert: Check if the value as expected
        assert response.status_code == 200
        assert response.json()["name"] == default_company.name

    def test_update_company(self, client, default_company):
        # Arrange: Get the company id
        company_id = default_company.id

        # Arrange: Set new name
        new_name = "This is new name"

        # Act: Update it
        patch = client.patch(f"/companies/{company_id}", json={"name": new_name})
        assert patch.status_code == 200
        assert patch.json()["name"] == new_name

    def test_delete_company(self, client, default_company):
        # Arrange: Get the company id
        company_id = default_company.id

        # Act: Delete it
        delete = client.delete(f"/companies/{company_id}")
        assert delete.status_code == 200
        assert delete.json() == {"ok": True}

        # Assert: Check again
        get = client.get(f"/companies/{company_id}")
        assert get.status_code == 404
