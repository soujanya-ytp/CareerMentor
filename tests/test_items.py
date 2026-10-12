from fastapi.testclient import TestClient


def test_create_and_fetch_item(client: TestClient) -> None:
    create_response = client.post(
        "/api/v1/items",
        json={"name": "First item", "description": "Created in a test"},
    )

    assert create_response.status_code == 201
    created_item = create_response.json()
    assert created_item["id"] == 1
    assert created_item["name"] == "First item"
    assert created_item["description"] == "Created in a test"

    list_response = client.get("/api/v1/items")
    assert list_response.status_code == 200
    assert list_response.json() == [created_item]

    get_response = client.get(f"/api/v1/items/{created_item['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == created_item


def test_create_item_rejects_duplicate_name(client: TestClient) -> None:
    payload = {"name": "Duplicate", "description": "first"}

    first_response = client.post("/api/v1/items", json=payload)
    duplicate_response = client.post("/api/v1/items", json=payload)

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 409
    assert duplicate_response.json() == {
        "detail": "Item with this name already exists"
    }


def test_get_missing_item_returns_404(client: TestClient) -> None:
    response = client.get("/api/v1/items/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
