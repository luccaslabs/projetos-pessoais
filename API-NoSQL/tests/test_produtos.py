from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_admin_user

client = TestClient(app)

def fake_admin():
    return {
        "uid": "admin123",
        "email": "admin@test.com",
        "admin": True
    }


app.dependency_overrides[get_admin_user] = fake_admin

def test_criar_produto():
    payload = {
        "nome": "Ração Golden",
        "categoria": "racao",
        "preco": 120.0,
        "fotos": ["foto1.jpg"],
        "descricao": "Ração premium",
        "estoque": 10
    }

    response = client.post("/produtos/", json=payload)

    print(response.json())

    assert response.status_code == 200

def test_listar_produtos():
    response = client.get("/produtos/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)