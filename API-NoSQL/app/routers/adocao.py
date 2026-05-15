from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, File
from app.schemas.animal import Anuncio, AnuncioForm
from app.dependencies import get_current_user
from app.services import anuncio_service

adocao_router = APIRouter(prefix="/adocao", tags=["adocoes"])

@adocao_router.post("/colocar_adocao")
async def criar_anuncio(
    anuncio: AnuncioForm = Depends(),
    fotos: List[UploadFile] = File(...),
    user=Depends(get_current_user)
):
    return await anuncio_service.create_anuncio(
        anuncio_data=vars(anuncio),
        fotos=fotos,
        uid=user["uid"]
    )

@adocao_router.put("/{anuncio_id}")
async def atualizar_anuncio(anuncio_id: str, anuncio: Anuncio, user=Depends(get_current_user)):
    return anuncio_service.update_anuncio(anuncio_id=anuncio_id, anuncio_data=anuncio.model_dump(), uid=user["uid"])

@adocao_router.get("/")
async def listar_anuncios(
    tipo: Optional[str] = None,
    porte: Optional[str] = None,
    cidade: Optional[str] = None,
    estado: Optional[str] = None,
    faixa_etaria: Optional[str] = None
):
    return anuncio_service.listar_anuncios(tipo=tipo, porte=porte, cidade=cidade, estado=estado, faixa_etaria=faixa_etaria)

@adocao_router.patch("/{anuncio_id}/indisponivel")
async def anuncio_indisponivel(anuncio_id: str, user=Depends(get_current_user)):
    return anuncio_service.anuncio_indisponivel(anuncio_id=anuncio_id, uid=user["uid"])

@adocao_router.patch("/{anuncio_id}/reativar")
async def reativar_anuncio(anuncio_id: str, user=Depends(get_current_user)):
    return anuncio_service.reativar_anuncio(anuncio_id=anuncio_id, uid=user["uid"])

@adocao_router.delete("/{anuncio_id}")
async def deletar_anuncio(anuncio_id: str, user=Depends(get_current_user)):
    return anuncio_service.deletar_anuncio(anuncio_id=anuncio_id, uid=user["uid"])