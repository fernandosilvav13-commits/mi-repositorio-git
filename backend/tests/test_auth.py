from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_auth_me_dev_bypass():
    resp = client.get("/api/auth/me")
    assert resp.status_code == 200
    assert resp.json()["sub"] == "dev-user"


def test_classify_responds_in_dev():
    resp = client.post("/api/classify/classify", json={"text": "test"})
    assert resp.status_code == 200
