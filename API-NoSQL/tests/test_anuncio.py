import pytest
import io
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_current_user

def mock_get_current_user():
    return {"uid": "teste_uid", "email": "teste@exemplo.com", "role": "user"}

app.dependency_overrides[get_current_user] = mock_get_current_user
client = TestClient(app)

def test_rotas():
    response = client.get("/openapi.json")
    import json
    print(json.dumps(response.json()["paths"], indent=2))

def test_criar_anuncio():
    foto_fake = io.BytesIO(b"fake image content")

    response = client.post(
        "/adocao/colocar_adocao",
        data={
            "nome": "Rex",
            "faixa_etaria": "adulto",
            "cor": "marrom",
            "raca": "vira-lata",
            "porte": "medio",
            "tipo": "cachorro",
            "historico_saude": "Vacinas em dia, sem doenças conhecidas.",
            "contato": "11987654321",
            "cep": "01310100"
        },
        files={"fotos": ("rex.jpg", foto_fake, "image/jpeg")}
    )

    print(response.json())
    assert response.status_code == 200
    assert response.status_code == 200
    assert "id" in response.json()
