from pydantic import BaseModel, Field, field_validator
from enum import Enum
import re
from typing import List
from fastapi import Form

class AnuncioForm:
    def __init__(
        self,
        nome: str = Form(...),
        faixa_etaria: str = Form(...),
        cor: str = Form(...),
        raca: str = Form(...),
        porte: str = Form(...),
        tipo: str = Form(...),
        historico_saude: str = Form(...),
        contato: str = Form(...),
        cep: str = Form(...)
    ):
        self.nome = nome
        self.faixa_etaria = faixa_etaria
        self.cor = cor
        self.raca = raca
        self.porte = porte
        self.tipo = tipo
        self.historico_saude = historico_saude
        self.contato = contato
        self.cep = cep


class TipoAnimal(str, Enum):
    cachorro = "cachorro"
    gato = "gato"

class Porte(str, Enum):
    pequeno = "pequeno"
    medio = "medio"
    grande = "grande"

class StatusAnuncio(str, Enum):
    disponivel = "disponivel"
    indisponivel = "indisponivel"

class FaixaEtaria(str, Enum):
    filhote = "filhote"
    adulto = "adulto"
    idoso = "idoso"

class Anuncio(BaseModel):
    #anuncio-animal
    nome: str = Field(min_length=1, max_length=50)
    faixa_etaria: FaixaEtaria
    cor: str = Field(min_length=1, max_length=30)
    raca: str = Field(min_length=1, max_length=50)
    porte: Porte
    tipo: TipoAnimal
    historico_saude: str = Field(min_length=20, max_length=500)
    contato: str = Field(min_length=11, max_length=11)
    fotos: List[str]
    cep: str = Field(min_length=8, max_length=8)
    
    @field_validator("nome", "cor", "raca")
    @classmethod
    def string_formatada(cls, s: str):
        if not s.strip():
            raise ValueError("Campo não pode ser vazio")
        return s.strip().title()
    
    @field_validator("historico_saude")
    @classmethod
    def validar_historico(cls, d: str):
        if not d.strip():
            raise ValueError("Histórico de saúde não pode ser vazio")
        return d.strip()

    @field_validator("contato")
    @classmethod
    def validar_contato(cls, c: str):
        numero = re.sub(r"\D", "", c)

        if len(numero) != 11:
            raise ValueError("Informe um celular válido com DDD (11 dígitos)")
        
        return numero
    
    @field_validator("cep")
    @classmethod
    def validar_cep(cls, c: str):
        cep = re.sub(r"\D", "", c)

        if len(cep) != 8:
            raise ValueError("CEP inválido")

        return cep
    
