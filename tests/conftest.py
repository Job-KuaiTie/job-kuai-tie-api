from fastapi.testclient import TestClient
from app.main import app
import pytest


@pytest.fixture(scope="session")
def client():
    yield TestClient(app)
