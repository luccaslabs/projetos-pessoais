import requests
from datetime import datetime, timezone
from fastapi import HTTPException
from app.external_services.firebase import db
from app.schemas.solicitacao import StatusSolicitacao
from app.schemas.animal import StatusAnuncio
from google.cloud.firestore_v1.base_query import FieldFilter


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


def create_solicitacao(solicitacao_data: dict, uid: str):
    anuncio_ref = db.collection("anuncios_animais").document(solicitacao_data["anuncio_id"])
    anuncio = anuncio_ref.get()

    if not anuncio.exists:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado")

    anuncio_data = anuncio.to_dict()

    if not anuncio_data["ativo"]:
        raise HTTPException(status_code=400, detail="Anúncio removido")

    if anuncio_data["status"] != StatusAnuncio.disponivel.value:
        raise HTTPException(status_code=400, detail="Pet não está disponível")

    if anuncio_data["owner_id"] == uid:
        raise HTTPException(status_code=400, detail="Você não pode solicitar o próprio anúncio")

    existing = (
    db.collection("solicitacoes")
      .where(filter=FieldFilter("uid", "==", uid))
      .where(filter=FieldFilter("anuncio_id", "==", solicitacao_data["anuncio_id"]))
      .where(filter=FieldFilter("status", "==", StatusSolicitacao.em_andamento.value))
      .limit(1)
      .stream()
)

    if any(existing):
        raise HTTPException(status_code=400, detail="Já existe uma solicitação em andamento")

    cep_data = validar_cep(solicitacao_data["cep"])

    data = {
        **solicitacao_data,
        "uid": uid,
        "rua": cep_data["logradouro"],
        "bairro": cep_data["bairro"],
        "cidade": cep_data["localidade"],
        "estado": cep_data["uf"],
        "status": StatusSolicitacao.em_andamento.value,
        "created_at": now()
    }

    _, doc_ref = db.collection("solicitacoes").add(data)
    return {"id": doc_ref.id, "mensagem": "Solicitação enviada com sucesso"}


def listar_solicitacoes():
    docs = (
        db.collection("solicitacoes")
        .order_by("created_at", direction="DESCENDING")
        .stream()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


def listar_solicitacoes_user(uid: str):
    docs = (
        db.collection("solicitacoes")
        .where("uid", "==", uid)
        .order_by("created_at", direction="DESCENDING")
        .stream()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


def atualizar_status_solicitacao(solicitacao_id: str, status: str):
    doc_ref = db.collection("solicitacoes").document(solicitacao_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")

    data = doc.to_dict()

    if data["status"] != StatusSolicitacao.em_andamento.value:
        raise HTTPException(status_code=400, detail="Solicitação já encerrada")

    if status not in [StatusSolicitacao.aprovado.value, StatusSolicitacao.negado.value]:
        raise HTTPException(status_code=400, detail="Status inválido")

    timestamp = now()
    doc_ref.update({"status": status, "updated_at": timestamp})

    if status == StatusSolicitacao.aprovado.value:
        anuncio_ref = db.collection("anuncios_animais").document(data["anuncio_id"])
        anuncio_doc = anuncio_ref.get()

        if not anuncio_doc.exists:
            raise HTTPException(status_code=404, detail="Anúncio não encontrado")

        if anuncio_doc.to_dict()["status"] != StatusAnuncio.disponivel.value:
            raise HTTPException(status_code=400, detail="Pet já adotado")

        anuncio_ref.update({"status": StatusAnuncio.indisponivel.value, "updated_at": timestamp})

        outras = (
            db.collection("solicitacoes")
            .where("anuncio_id", "==", data["anuncio_id"])
            .where("status", "==", StatusSolicitacao.em_andamento.value)
            .stream()
        )

        for s in outras:
            if s.id != solicitacao_id:
                db.collection("solicitacoes").document(s.id).update({
                    "status": StatusSolicitacao.negado.value,
                    "updated_at": timestamp
                })

    return {"mensagem": f"Solicitação {status} com sucesso"}