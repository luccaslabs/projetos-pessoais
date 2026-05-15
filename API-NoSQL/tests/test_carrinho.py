from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_current_user

client = TestClient(app)


def fake_user():
    return {
        "uid": "user123",
        "email": "user@test.com"
    }


app.dependency_overrides[get_current_user] = fake_user

def test_adicionar_item_carrinho():
    payload = {
        "produto_id": "b4FlzRUhovNG4YN3g9GN",
        "quantidade": 2
    }

    response = client.post("/carrinho/", json=payload)

    assert response.status_code == 200

def test_buscar_carrinho():
    response = client.get("/carrinho/")

    assert response.status_code == 200


def test_atualizar_item_carrinho():
    payload = {
        "produto_id": "b4FlzRUhovNG4YN3g9GN",
        "quantidade": 5
    }

    response = client.put("/carrinho/", json=payload)

    assert response.status_code == 200

def test_remover_item_carrinho():
    response = client.delete("/carrinho/b4FlzRUhovNG4YN3g9GN")

    assert response.status_code == 200