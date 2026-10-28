
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "running"


def test_create_request(client):
    response = client.post(
        "/requests",
        json={"title": "Test request"}
    )
    assert response.status_code == 201


def test_reject_empty_title(client):
    response = client.post("/requests", json={"title": ""})
    assert response.status_code == 400


def test_missing_request(client):
    response = client.get("/requests/999")
    assert response.status_code == 404


def test_read_created_request(client):
    response = client.post(
        "/requests",
        json={"title": "My request"}
    )
    request_id = response.json["id"]

    result = client.get(f"/requests/{request_id}")
    assert result.status_code == 200
    assert result.json["title"] == "My request"
