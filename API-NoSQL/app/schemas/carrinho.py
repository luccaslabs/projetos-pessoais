from pydantic import BaseModel, Field

class ItemCarrinho(BaseModel):
    produto_id: str
    quantidade: int = Field(gt=0)

class CarrinhoUpdate(BaseModel):
    produto_id: str
    quantidade: int

class Pedido(BaseModel):
    pass