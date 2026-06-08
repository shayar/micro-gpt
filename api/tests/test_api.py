from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_requires_authentication():
    response = client.post("/chat", json={"message": "hello"})
    assert response.status_code == 401
