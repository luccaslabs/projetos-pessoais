import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_current_user, get_admin_user

def mock_get_current_user():
    return {"uid": "teste2_uid", "email": "teste@exemplo.com", "role": "user"}

def mock_get_admin_user():
    return {"uid": "admin_uid", "email": "admin@exemplo.com", "role": "admin"}

app.dependency_overrides[get_current_user] = mock_get_current_user
app.dependency_overrides[get_admin_user] = mock_get_admin_user

client = TestClient(app)

def test_criar_solicitacao():
    payload = {
    "anuncio_id": "1VgxGOQaYYUse43fOgAc",
    "nome": "João Silva",
    "cpf": "529.982.247-25",
    "cep": "01310100",
    "numero": "100",
    "telefone": "11987654321",
    "motivo": "Quero adotar o pet pois tenho espaço e experiência com animais."
}

    response = client.post("/solicitacoes/", json=payload)
    
    print(response.json())
    assert response.status_code == 200
    assert "id" in response.json()

def test_listar_solicitacoes():
    response = client.get("/solicitacoes/")
    print(response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_minhas_solicitacoes():
    response = client.get("/solicitacoes/minhas")
    print(response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), list)