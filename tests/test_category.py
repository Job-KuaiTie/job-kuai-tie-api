class TestCategory:
    def test_create_category(self, client, default_account):
        name = "This is a chill category"
        color = "#FFFFFF"
        owner_id = default_account.id

        response = client.post(
            "/categories/",
            json={"name": name, "color": color, "owner_id": owner_id},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == name
        assert data["color"] == color
        assert data["owner_id"] == owner_id
        assert "id" in data

    def test_create_category_wihtou_color(self, client, default_account):
        name = "This is another chill category"
        owner_id = default_account.id

        response = client.post(
            "/categories/",
            json={"name": name, "owner_id": owner_id},
        )
        # Should return 422 Unprocessable Entity as lack of tier
        assert response.status_code == 422

    def test_read_categories(self, client):
        response = client.get("/categories/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_read_category(self, client, default_category):
        # Arrange: Get the category id
        category_id = default_category.id

        # Act: Read it back
        response = client.get(f"/categories/{category_id}")

        # Assert: Check if the value as expected
        assert response.status_code == 200
        assert response.json()["name"] == default_category.name

    def test_update_category(self, client, default_category):
        # Arrange: Get the category id
        category_id = default_category.id

        # Arrange: Set new name
        new_name = "This is new name"

        # Act: Update it
        patch = client.patch(
            f"/categories/{category_id}",
            json={"name": new_name, "owner_id": default_category.owner_id},
        )
        assert patch.status_code == 200
        assert patch.json()["name"] == new_name

    def test_delete_category(self, client, default_category):
        # Arrange: Get the category id
        category_id = default_category.id

        # Act: Delete it
        delete = client.delete(f"/categories/{category_id}")
        assert delete.status_code == 200
        assert delete.json() == {"ok": True}

        # Assert: Check again
        get = client.get(f"/categories/{category_id}")
        assert get.status_code == 404
