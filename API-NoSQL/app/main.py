from dotenv import load_dotenv
from fastapi import FastAPI
from app.external_services import firebase
from app.routers.auth import auth_router
from app.routers.adocao import adocao_router
from app.routers.solicitacao import solicitacao_router
from app.routers.carrinho import carrinho_router
from app.routers.produto import produto_router
import os
from fastapi.staticfiles import StaticFiles

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(auth_router)
app.include_router(adocao_router)
app.include_router(solicitacao_router)
app.include_router(carrinho_router)
app.include_router(produto_router)