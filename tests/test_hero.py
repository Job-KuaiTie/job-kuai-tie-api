from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_hero():
    response = client.post(
        "/heroes/", json={"name": "Test Hero", "age": 30, "secret_name": "Secret"}
    )
    assert response.status_code == 200
    data = response.json()
    breakpoint()
    assert data["name"] == "Test Hero"
    assert "id" in data


def test_read_heroes():
    response = client.get("/heroes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_hero():
    # Create one first
    post = client.post(
        "/heroes/", json={"name": "Test Read", "age": 25, "secret_name": "ReadSecret"}
    )
    hero_id = post.json()["id"]

    # Read it back
    response = client.get(f"/heroes/{hero_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Read"


def test_update_hero():
    # Create one first
    post = client.post(
        "/heroes/",
        json={"name": "Test Update", "age": 35, "secret_name": "UpdateSecret"},
    )
    hero_id = post.json()["id"]

    # Update it
    patch = client.patch(f"/heroes/{hero_id}", json={"age": 40})
    assert patch.status_code == 200
    assert patch.json()["age"] == 40


def test_delete_hero():
    # Create one first
    post = client.post(
        "/heroes/",
        json={"name": "Test Delete", "age": 22, "secret_name": "DeleteSecret"},
    )
    hero_id = post.json()["id"]

    # Delete it
    delete = client.delete(f"/heroes/{hero_id}")
    assert delete.status_code == 200
    assert delete.json() == {"ok": True}

    # Check again
    get = client.get(f"/heroes/{hero_id}")
    assert get.status_code == 404
