from pydantic import BaseModel, Field, field_validator
from enum import Enum
import re


class StatusSolicitacao(str, Enum):
    em_andamento = "em andamento"
    aprovado = "aprovado"
    negado = "negado"


class Solicitacao(BaseModel):
    anuncio_id: str = Field(min_length=1)
    nome: str = Field(min_length=3, max_length=100)
    telefone: str
    cep: str
    numero: str = Field(min_length=1, max_length=20)
    complemento: str | None = Field(
        default=None,
        max_length=100
    )
    motivo: str = Field(
        min_length=10,
        max_length=500
    )

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v: str):
        if not v.strip():
            raise ValueError(
                "Nome não pode ser vazio"
            )

        return v.strip().title()

    @field_validator("telefone")
    @classmethod
    def validar_telefone(cls, v: str):
        numero = re.sub(r"\D", "", v)

        if len(numero) != 11:
            raise ValueError(
                "Telefone inválido"
            )

        return numero

    @field_validator("cep")
    @classmethod
    def validar_cep(cls, v: str):
        cep = re.sub(r"\D", "", v)

        if len(cep) != 8:
            raise ValueError(
                "CEP inválido"
            )

        return cep

    @field_validator("motivo")
    @classmethod
    def validar_motivo(cls, v: str):
        if not v.strip():
            raise ValueError(
                "Motivo não pode ser vazio"
            )

        return v.strip()