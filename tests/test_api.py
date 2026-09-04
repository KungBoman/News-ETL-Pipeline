from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.stat_code == 200
    assert response.json()["name"] == "Swedish News ETL API"
