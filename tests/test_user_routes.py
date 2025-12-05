import pytest

from uuid import uuid4


@pytest.fixture()
def user_payload():
    def _factory(suffix=None):
        token = suffix or uuid4().hex[:8]
        return {"username": f"alice-{token}", "email": f"alice-{token}@example.com"}

    return _factory


def test_list_users_returns_empty_success(client):
    response = client.get("/api/users")
    body = response.get_json()

    assert response.status_code == 200
    assert body["status"] == "success"
    assert body["count"] == 0
    assert body["users"] == []


def test_create_and_fetch_user(client, user_payload):
    payload = user_payload()
    create = client.post("/api/users", json=payload)
    created_body = create.get_json()

    assert create.status_code == 201
    assert created_body["status"] == "success"
    user_id = created_body["user"]["id"]

    fetched = client.get(f"/api/users/{user_id}")
    fetched_body = fetched.get_json()

    assert fetched.status_code == 200
    assert fetched_body["user"]["username"] == payload["username"]
    assert fetched_body["user"]["email"] == payload["email"]


def test_create_user_requires_fields(client):
    missing = client.post("/api/users", json={})
    assert missing.status_code == 400
    assert missing.get_json()["message"] == "Username and email are required"

    invalid = client.post("/api/users", data="not-json", content_type="text/plain")
    assert invalid.status_code == 400
    assert invalid.get_json()["message"] == "Invalid JSON payload"


def test_update_user_validates_payload(client, user_payload):
    created = client.post("/api/users", json=user_payload()).get_json()
    user_id = created["user"]["id"]

    no_fields = client.put(f"/api/users/{user_id}", json={})
    assert no_fields.status_code == 400

    update = client.put(
        f"/api/users/{user_id}", json={"username": "alice-updated", "email": "new@example.com"}
    )
    assert update.status_code == 200
    updated_body = update.get_json()["user"]
    assert updated_body["username"] == "alice-updated"
    assert updated_body["email"] == "new@example.com"


def test_delete_user(client, user_payload):
    created = client.post("/api/users", json=user_payload()).get_json()
    user_id = created["user"]["id"]

    deleted = client.delete(f"/api/users/{user_id}")
    assert deleted.status_code == 204

    missing = client.get(f"/api/users/{user_id}")
    assert missing.status_code == 404


def test_duplicate_user_rejected(client, user_payload):
    base_user = user_payload("duplicate")
    client.post("/api/users", json=base_user)
    duplicate = client.post("/api/users", json=base_user)

    assert duplicate.status_code == 409
    assert duplicate.get_json()["message"] == "User with this username or email already exists"
