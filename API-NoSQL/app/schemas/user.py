from pydantic import BaseModel, EmailStr, field_validator
import re

class Login(BaseModel):
    email: str
    senha: str

class Usuario(BaseModel):
    nome: str
    email: EmailStr
    senha: str

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, s: str):
        if len(s) < 8:
            raise ValueError("Senha deve ter no mínimo 8 caracteres")
        if not re.search(r"[A-Za-z]", s):
            raise ValueError("Senha precisa ter pelo menos uma letra")
        
        if not re.search(r"\d", s):
            raise ValueError("Senha precisa ter pelo menos um número")
        
        return s
    
    @field_validator("nome")
    @classmethod
    def validar_nome(cls, n):
        if not n.strip():
            raise ValueError("Nome não pode ser vazio")
        if len(n.strip()) > 100:
            raise ValueError("Nome muito longo") 
        
        return n.strip()

