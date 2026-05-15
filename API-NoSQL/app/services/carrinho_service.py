from decimal import Decimal
from fastapi import HTTPException
from google.cloud import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
from app.external_services.firebase import db

def get_carrinho(uid: str):
    doc_ref = db.collection("carrinhos").document(uid)
    doc = doc_ref.get()

    itens = []

    if doc.exists:
        data = doc.to_dict()
        itens = data.get("itens", [])

    return doc_ref, itens


def validar_quantidade(quantidade: int):
    if quantidade <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantidade deve ser maior que zero"
        )

def adicionar_item(uid: str, produto_id: str, quantidade: int):
    validar_quantidade(quantidade)

    produto_ref = db.collection("produtos").document(produto_id)
    produto = produto_ref.get()

    if not produto.exists:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    produto_data = produto.to_dict()

    if not produto_data.get("ativo", False):
        raise HTTPException(
            status_code=400,
            detail="Produto indisponível"
        )

    estoque = produto_data.get("estoque")

    if estoque is None:
        raise HTTPException(
            status_code=500,
            detail="Produto sem estoque definido"
        )

    if estoque < quantidade:
        raise HTTPException(
            status_code=400,
            detail="Estoque insuficiente"
        )

    doc_ref, itens = get_carrinho(uid)

    item_existente = next(
        (item for item in itens if item["produto_id"] == produto_id),
        None
    )

    if item_existente:
        item_existente["quantidade"] += quantidade
    else:
        itens.append({
            "produto_id": produto_id,
            "quantidade": quantidade
        })

    doc_ref.set(
        {
            "itens": itens,
            "updated_at": SERVER_TIMESTAMP
        },
        merge=True
    )

    return {"mensagem": "Carrinho atualizado"}

def atualizar_item(payload):
    carrinho_ref = db.collection("carrinho")

    docs = carrinho_ref.where(
        "produto_id", "==", payload.produto_id
    ).stream()

    doc = next(docs, None)

    if not doc:
        return {"mensagem": "Produto não encontrado no carrinho"}

    doc.reference.update({
        "quantidade": payload.quantidade
    })

    return {"mensagem": "Carrinho atualizado"}


def remover_item(uid: str, produto_id: str):
    doc_ref, itens = get_carrinho(uid)

    novos_itens = [
        item for item in itens
        if item["produto_id"] != produto_id
    ]

    if len(novos_itens) == len(itens):
        raise HTTPException(
            status_code=404,
            detail="Item não encontrado no carrinho"
        )

    doc_ref.set(
        {
            "itens": novos_itens,
            "updated_at": SERVER_TIMESTAMP
        },
        merge=True
    )

    return {"mensagem": "Item removido do carrinho"}


def listar_carrinho(uid: str):
    _, itens = get_carrinho(uid)
    return itens

@firestore.transactional
def finalizar_compra_transaction(transaction, uid: str):

    carrinho_ref = db.collection("carrinhos").document(uid)
    carrinho_snapshot = carrinho_ref.get(transaction=transaction)

    if not carrinho_snapshot.exists:
        raise HTTPException(
            status_code=400,
            detail="Carrinho vazio"
        )

    carrinho_data = carrinho_snapshot.to_dict()
    itens = carrinho_data.get("itens", [])

    if not itens:
        raise HTTPException(
            status_code=400,
            detail="Carrinho vazio"
        )

    total = Decimal("0.00")
    itens_pedido = []
    produtos_refs = [db.collection("produtos").document(item["produto_id"]) for item in itens]
    produtos_snapshots = [ref.get(transaction=transaction) for ref in produtos_refs]

    for item, produto_snapshot in zip(itens, produtos_snapshots):

        if not produto_snapshot.exists:
            raise HTTPException(
                status_code=404,
                detail=f"Produto {item['produto_id']} não encontrado"
            )

        produto_data = produto_snapshot.to_dict()

        if not produto_data.get("ativo", False):
            raise HTTPException(
                status_code=400,
                detail=f"Produto {produto_data.get('nome')} indisponível"
            )

        estoque = produto_data.get("estoque", 0)

        if estoque < item["quantidade"]:
            raise HTTPException(
                status_code=400,
                detail=f"Estoque insuficiente para {produto_data.get('nome')}"
            )

        preco = Decimal(str(produto_data.get("preco", 0)))
        subtotal = preco * item["quantidade"]
        total += subtotal

        itens_pedido.append({
            "produto_id": item["produto_id"],
            "nome": produto_data.get("nome"),
            "preco": float(preco),
            "quantidade": item["quantidade"],
            "subtotal": float(subtotal)
        })

        novo_estoque = estoque - item["quantidade"]

        transaction.update(
            produto_snapshot.reference,
            {
                "estoque": novo_estoque,
                "updated_at": SERVER_TIMESTAMP
            }
        )

    pedido_ref = db.collection("pedidos").document()

    transaction.set(
        pedido_ref,
        {
            "uid": uid,
            "itens": itens_pedido,
            "total": float(total),
            "status": "aguardando_pagamento",
            "created_at": SERVER_TIMESTAMP
        }
    )

    transaction.set(
        carrinho_ref,
        {
            "itens": [],
            "updated_at": SERVER_TIMESTAMP
        },
        merge=True
    )

    return {
        "id": pedido_ref.id,
        "total": float(total),
        "mensagem": "Compra finalizada com sucesso"
    }


def finalizar_compra(uid: str):
    transaction = db.transaction()
    return finalizar_compra_transaction(transaction, uid)
