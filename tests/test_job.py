class TestJob:
    def test_create_job(self, client, default_account):
        name = "This is a chill job"
        tier = 1
        url = "https://thisisachilljob.com/"
        owner_id = default_account.id

        response = client.post(
            "/jobs/",
            json={"name": name, "tier": tier, "url": url, "owner_id": owner_id},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == name
        assert data["tier"] == tier
        assert data["url"] == url
        assert data["owner_id"] == owner_id
        assert "id" in data

    def test_create_job_wihtou_tier(self, client, default_account):
        name = "This is a chill job"
        url = "https://thisisachilljob.com/"
        owner_id = default_account.id

        response = client.post(
            "/jobs/",
            json={"name": name, "url": url, "owner_id": owner_id},
        )
        # Should return 422 Unprocessable Entity as lack of tier
        assert response.status_code == 422

    def test_read_jobs(self, client):
        response = client.get("/jobs/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_read_job(self, client, default_job):
        # Arrange: Get the job id
        job_id = default_job.id

        # Act: Read it back
        response = client.get(f"/jobs/{job_id}")

        # Assert: Check if the value as expected
        assert response.status_code == 200
        assert response.json()["name"] == default_job.name

    def test_update_job(self, client, default_job):
        # Arrange: Get the job id
        job_id = default_job.id

        # Arrange: Set new name
        new_name = "This is new name"

        # Act: Update it
        patch = client.patch(
            f"/jobs/{job_id}",
            json={"name": new_name, "owner_id": default_job.owner_id},
        )
        assert patch.status_code == 200
        assert patch.json()["name"] == new_name

    def test_delete_job(self, client, default_job):
        # Arrange: Get the job id
        job_id = default_job.id

        # Act: Delete it
        delete = client.delete(f"/jobs/{job_id}")
        assert delete.status_code == 200
        assert delete.json() == {"ok": True}

        # Assert: Check again
        get = client.get(f"/jobs/{job_id}")
        assert get.status_code == 404
