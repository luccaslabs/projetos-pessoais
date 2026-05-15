from fastapi import APIRouter, Depends
from app.schemas.carrinho import ItemCarrinho, CarrinhoUpdate
from app.dependencies import get_current_user
from app.services import carrinho_service

carrinho_router = APIRouter(prefix="/carrinho", tags=["carrinho"])

@carrinho_router.get("/")
async def listar_carrinho(user=Depends(get_current_user)):
    return carrinho_service.listar_carrinho(uid=user["uid"])

@carrinho_router.post("/")
async def adicionar_item(item: ItemCarrinho, user=Depends(get_current_user)):
    return carrinho_service.adicionar_item(
        uid=user["uid"],
        produto_id=item.produto_id,
        quantidade=item.quantidade
    )

@carrinho_router.put("/")
async def atualizar_item_carrinho(payload: CarrinhoUpdate):
    return carrinho_service.atualizar_item(payload)

@carrinho_router.delete("/{produto_id}")
async def remover_item(produto_id: str, user=Depends(get_current_user)):
    return carrinho_service.remover_item(uid=user["uid"], produto_id=produto_id)

@carrinho_router.post("/finalizar")
async def finalizar_compra(user=Depends(get_current_user)):
    return carrinho_service.finalizar_compra(uid=user["uid"])