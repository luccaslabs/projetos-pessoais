from fastapi import APIRouter, Depends
from app.schemas.solicitacao import Solicitacao
from app.dependencies import get_current_user, get_admin_user
from app.services import solicitacao_service

solicitacao_router = APIRouter(prefix="/solicitacoes", tags=["solicitacoes"])

@solicitacao_router.post("/")
async def criar_solicitacao(
    solicitacao: Solicitacao,
    user=Depends(get_current_user)
):
    return solicitacao_service.create_solicitacao(
        solicitacao_data=solicitacao.model_dump(),
        uid=user["uid"]
    )

@solicitacao_router.get("/")
async def listar(user=Depends(get_admin_user)):
    return solicitacao_service.listar_solicitacoes()

@solicitacao_router.get("/minhas")
async def minhas_solicitacoes(user=Depends(get_current_user)):
    return solicitacao_service.listar_solicitacoes_user(uid=user["uid"])

@solicitacao_router.put("/{solicitacao_id}")
async def atualizar_status(
    solicitacao_id: str,
    status: str,
    user=Depends(get_admin_user)
):
    return solicitacao_service.atualizar_status_solicitacao(
        solicitacao_id=solicitacao_id,
        status=status
    )