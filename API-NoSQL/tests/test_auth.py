from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup():
    response = client.post("/auth/signup", json={
        "email": "teste1@gmail.com",
        "senha": "a12345678",
        "nome": "Lucas"
    })

    assert response.status_code == 200
    assert "uid" in response.json()