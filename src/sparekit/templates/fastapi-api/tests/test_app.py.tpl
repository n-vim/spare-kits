from fastapi.testclient import TestClient

from {{ package_name }}.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_hello() -> None:
    response = client.get("/api/v1/hello", params={"name": "SpareKit"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, SpareKit!"}
