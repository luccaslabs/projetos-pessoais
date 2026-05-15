from pydantic import BaseModel, Field
from enum import Enum
from typing import List

class Categoria(str, Enum):
    racao = "racao"
    acessorios = "acessorios"
    brinquedos = "brinquedos"
    higiene = "higiene"

class Produto(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    categoria: Categoria
    preco: float = Field(..., gt=0)
    estoque: int = Field(..., ge=0)
    descricao: str = Field(..., min_length=5)
    fotos: List[str] = Field(default_factory=list)

class ProdutoResponse(Produto):
    id: str
    ativo: bool
    created_at: str
    updated_at: str