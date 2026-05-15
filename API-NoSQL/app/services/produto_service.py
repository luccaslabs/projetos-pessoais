from fastapi import HTTPException
from google.cloud.firestore import Query
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
from google.cloud.firestore_v1.base_query import FieldFilter

from app.external_services.firebase import db

def get_produto(produto_id: str):
    doc_ref = db.collection("produtos").document(produto_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    data = doc.to_dict()

    if not data.get("ativo", False):
        raise HTTPException(
            status_code=404,
            detail="Produto indisponível"
        )

    return doc_ref, data

def create_produto(produto_data: dict):
    data = {
        **produto_data,
        "ativo": True,
        "created_at": SERVER_TIMESTAMP,
        "updated_at": SERVER_TIMESTAMP
    }

    doc_ref = db.collection("produtos").document()
    doc_ref.set(data)

    return {
        "id": doc_ref.id,
        "mensagem": "Produto cadastrado com sucesso"
    }

def update_produto(produto_id: str, produto_data: dict):
    doc_ref, _ = get_produto(produto_id)

    campos_permitidos = {
        "nome",
        "descricao",
        "preco",
        "estoque",
        "categoria",
        "fotos"
    }

    dados_filtrados = {
        k: v
        for k, v in produto_data.items()
        if k in campos_permitidos
    }

    if not dados_filtrados:
        raise HTTPException(
            status_code=400,
            detail="Nenhum campo válido enviado"
        )

    dados_filtrados["updated_at"] = SERVER_TIMESTAMP
    doc_ref.update(dados_filtrados)

    return {"mensagem": "Produto atualizado com sucesso"}

def listar_produtos(categoria: str | None = None):
    query = (
        db.collection("produtos")
        .where(filter=FieldFilter("ativo", "==", True))
    )

    if categoria:
        query = query.where(
            filter=FieldFilter("categoria", "==", categoria)
        )

    docs = (
        query
        .order_by("created_at", direction=Query.DESCENDING)
        .limit(20)
        .stream()
    )

    return [
        {
            "id": doc.id,
            **doc.to_dict()
        }
        for doc in docs
    ]

def deletar_produto(produto_id: str):
    doc_ref, _ = get_produto(produto_id)

    doc_ref.update({
        "ativo": False,
        "updated_at": SERVER_TIMESTAMP
    })

    return {"mensagem": "Produto removido"}
