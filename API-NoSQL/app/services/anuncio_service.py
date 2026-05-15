import requests
from datetime import datetime, timezone
from fastapi import HTTPException
from app.external_services.firebase import db
from app.schemas.animal import StatusAnuncio
from app.utils.upload import salvar_imagem


def now():
    return datetime.now(timezone.utc).isoformat()


def validar_cep(cep: str):
    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5)
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Erro ao consultar CEP")

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="CEP inválido")

    data = response.json()

    if "erro" in data:
        raise HTTPException(status_code=400, detail="CEP não encontrado")

    return data


def get_anuncio(anuncio_id: str):
    doc_ref = db.collection("anuncios_animais").document(anuncio_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado")

    return doc_ref, doc.to_dict()


def validar_owner(data: dict, uid: str):
    if data["owner_id"] != uid:
        raise HTTPException(status_code=403, detail="Acesso negado")


def validar_anuncio_ativo(data: dict):
    if not data["ativo"]:
        raise HTTPException(status_code=400, detail="Anúncio já foi removido")


async def create_anuncio(anuncio_data: dict, fotos, uid: str):
    fotos_urls = []

    for foto in fotos:
        url = await salvar_imagem(foto)
        fotos_urls.append(url)

    cep_data = validar_cep(anuncio_data["cep"])
    timestamp = now()

    data = {
        **anuncio_data,
        "fotos": fotos_urls,
        "cidade": cep_data["localidade"],
        "estado": cep_data["uf"],
        "owner_id": uid,
        "status": StatusAnuncio.disponivel.value,
        "ativo": True,
        "created_at": timestamp
    }

    _, doc_ref = db.collection("anuncios_animais").add(data)

    return {"id": doc_ref.id, "mensagem": "Anúncio cadastrado com sucesso"}

def update_anuncio(anuncio_id: str, anuncio_data: dict, uid: str):
    doc_ref, data = get_anuncio(anuncio_id)

    validar_anuncio_ativo(data)
    validar_owner(data, uid)

    if data["status"] == StatusAnuncio.indisponivel.value:
        raise HTTPException(status_code=400, detail="Não é possível editar um anúncio indisponível")

    for campo in ["owner_id", "status", "ativo", "cidade", "estado", "created_at", "updated_at"]:
        anuncio_data.pop(campo, None)

    if "cep" in anuncio_data:
        cep_data = validar_cep(anuncio_data["cep"])
        anuncio_data["cidade"] = cep_data["localidade"]
        anuncio_data["estado"] = cep_data["uf"]

    doc_ref.update({**anuncio_data, "updated_at": now()})
    return {"mensagem": "Anúncio atualizado com sucesso"}


def listar_anuncios(tipo=None, porte=None, cidade=None, estado=None, faixa_etaria=None):
    query = (
        db.collection("anuncios_animais")
        .where("ativo", "==", True)
        .where("status", "==", StatusAnuncio.disponivel.value)
    )

    if tipo:
        query = query.where("tipo", "==", tipo)
    if porte:
        query = query.where("porte", "==", porte)
    if cidade:
        query = query.where("cidade", "==", cidade.title())
    if estado:
        query = query.where("estado", "==", estado.upper())
    if faixa_etaria:
        query = query.where("faixa_etaria", "==", faixa_etaria)

    docs = query.order_by("created_at", direction="DESCENDING").limit(20).stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


def anuncio_indisponivel(anuncio_id: str, uid: str):
    doc_ref, data = get_anuncio(anuncio_id)

    validar_anuncio_ativo(data)
    validar_owner(data, uid)

    if data["status"] == StatusAnuncio.indisponivel.value:
        raise HTTPException(status_code=400, detail="Anúncio já está indisponível")

    doc_ref.update({"status": StatusAnuncio.indisponivel.value, "updated_at": now()})
    return {"mensagem": "Anúncio indisponível"}


def reativar_anuncio(anuncio_id: str, uid: str):
    doc_ref, data = get_anuncio(anuncio_id)

    validar_anuncio_ativo(data)
    validar_owner(data, uid)

    if data["status"] == StatusAnuncio.disponivel.value:
        raise HTTPException(status_code=400, detail="Anúncio já está disponível")

    doc_ref.update({"status": StatusAnuncio.disponivel.value, "updated_at": now()})
    return {"mensagem": "Anúncio reativado"}


def deletar_anuncio(anuncio_id: str, uid: str):
    doc_ref, data = get_anuncio(anuncio_id)

    validar_anuncio_ativo(data)
    validar_owner(data, uid)

    doc_ref.update({"ativo": False, "status": StatusAnuncio.indisponivel.value, "updated_at": now()})
    return {"mensagem": "Anúncio removido"}