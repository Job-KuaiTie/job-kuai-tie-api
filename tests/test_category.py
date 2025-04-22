from tests.factory import create_account, create_category


class TestCategory:
    def test_create_category(self, client, default_account, default_token):
        name = "This is a chill category"
        color = "#FFFFFF"

        response = client.post(
            "/categories/",
            json={"name": name, "color": color},
            headers={"Authorization": f"Bearer {default_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == name
        assert data["color"] == color
        assert "id" in data

    def test_create_category_without_color(
        self, client, default_account, default_token
    ):
        name = "This is another chill category"

        response = client.post(
            "/categories/",
            json={"name": name},
            headers={"Authorization": f"Bearer {default_token}"},
        )
        # Should return 422 Unprocessable Entity as lack of tier
        assert response.status_code == 422

    def test_read_categories(self, client, default_token):
        response = client.get(
            "/categories/", headers={"Authorization": f"Bearer {default_token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_read_category(self, client, default_category, default_token):
        # Arrange: Get the category id
        category_id = default_category.id

        # Act: Read it back
        response = client.get(
            f"/categories/{category_id}",
            headers={"Authorization": f"Bearer {default_token}"},
        )

        # Assert: Check if the value as expected
        assert response.status_code == 200
        assert response.json()["name"] == default_category.name

    def test_read_others_category(self, client, session, default_token):
        # Arrange: Create another account
        another_account = create_account(session)

        # Arrange: Create another category belong to that account
        another_category = create_category(another_account, session)

        # Arrange: Get the category id
        another_category_id = another_category.id

        # Act: Read it back
        response = client.get(
            f"/categories/{another_category_id}",
            headers={"Authorization": f"Bearer {default_token}"},
        )

        # Assert: CHeck other's resource should be 404
        assert response.status_code == 404

    def test_update_category(self, client, default_category, default_token):
        # Arrange: Get the category id
        category_id = default_category.id

        # Arrange: Set new name
        new_name = "This is new name"

        # Act: Update it
        patch = client.patch(
            f"/categories/{category_id}",
            json={"name": new_name},
            headers={"Authorization": f"Bearer {default_token}"},
        )
        assert patch.status_code == 200
        assert patch.json()["name"] == new_name

    def test_delete_category(self, client, default_category, default_token):
        # Arrange: Get the category id
        category_id = default_category.id

        # Act: Delete it
        delete = client.delete(
            f"/categories/{category_id}",
            headers={"Authorization": f"Bearer {default_token}"},
        )
        assert delete.status_code == 200
        assert delete.json() == {"ok": True}

        # Assert: Check again
        get = client.get(
            f"/categories/{category_id}",
            headers={"Authorization": f"Bearer {default_token}"},
        )
        assert get.status_code == 404
