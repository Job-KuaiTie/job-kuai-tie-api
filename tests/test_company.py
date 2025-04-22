from tests.factory import create_account, create_company


class TestCompany:
    def test_create_company(self, client, default_account, default_token):
        name = "This is a chill company"
        url = "https://thisisachillcompany.com/"
        size = 20

        response = client.post(
            "/companies/",
            json={"name": name, "url": url, "size": size},
            headers={"Authorization": f"Bearer {default_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == name
        assert data["url"] == url
        assert data["size"] == size
        assert "id" in data

    def test_read_companies(self, client, default_token):
        response = client.get(
            "/companies/", headers={"Authorization": f"Bearer {default_token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_read_company(self, client, default_company, default_token):
        # Arrange: Get the company id
        company_id = default_company.id

        # Act: Read it back
        response = client.get(
            f"/companies/{company_id}",
            headers={"Authorization": f"Bearer {default_token}"},
        )

        # Assert: Check if the value as expected
        assert response.status_code == 200
        assert response.json()["name"] == default_company.name

    def test_read_others_company(self, client, session, default_token):
        # Arrange: Create another account
        another_account = create_account(session)

        # Arrange: Create another company belong to that account
        another_company = create_company(another_account, session)

        # Arrange: Get the company id
        another_company_id = another_company.id

        # Act: Read it back
        response = client.get(
            f"/companies/{another_company_id}",
            headers={"Authorization": f"Bearer {default_token}"},
        )

        # Assert: CHeck other's resource should be 404
        assert response.status_code == 404

    def test_update_company(self, client, default_company, default_token):
        # Arrange: Get the company id
        company_id = default_company.id

        # Arrange: Set new name
        new_name = "This is new name"

        # Act: Update it
        patch = client.patch(
            f"/companies/{company_id}",
            json={"name": new_name},
            headers={"Authorization": f"Bearer {default_token}"},
        )
        assert patch.status_code == 200
        assert patch.json()["name"] == new_name

    def test_delete_company(self, client, default_company, default_token):
        # Arrange: Get the company id
        company_id = default_company.id

        # Act: Delete it
        delete = client.delete(
            f"/companies/{company_id}",
            headers={"Authorization": f"Bearer {default_token}"},
        )
        assert delete.status_code == 200
        assert delete.json() == {"ok": True}

        # Assert: Check again
        get = client.get(
            f"/companies/{company_id}",
            headers={"Authorization": f"Bearer {default_token}"},
        )
        assert get.status_code == 404
