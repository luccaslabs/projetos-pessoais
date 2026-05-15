from typing import Optional
from fastapi import APIRouter, Depends

from app.schemas.produtos import Produto, Categoria
from app.dependencies import get_admin_user
from app.services import produto_service

produto_router = APIRouter(
    prefix="/produtos",
    tags=["produtos"]
)

@produto_router.post("/")
async def criar_produto(
    produto: Produto,
    user=Depends(get_admin_user)
):
    return produto_service.create_produto(produto.model_dump())


@produto_router.put("/{produto_id}")
async def atualizar_produto(
    produto_id: str,
    produto: Produto,
    user=Depends(get_admin_user)
):
    return produto_service.update_produto(
        produto_id,
        produto.model_dump()
    )


@produto_router.get("/")
async def listar_produtos(
    categoria: Optional[Categoria] = None
):
    return produto_service.listar_produtos(
        categoria=categoria.value if categoria else None
    )


@produto_router.delete("/{produto_id}")
async def deletar_produto(
    produto_id: str,
    user=Depends(get_admin_user)
):
    return produto_service.deletar_produto(produto_id)