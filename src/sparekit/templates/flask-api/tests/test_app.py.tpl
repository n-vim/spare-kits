from {{ package_name }} import create_app


def test_health() -> None:
    client = create_app().test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_hello() -> None:
    client = create_app().test_client()
    response = client.get("/api/v1/hello?name=SpareKit")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello, SpareKit!"}
