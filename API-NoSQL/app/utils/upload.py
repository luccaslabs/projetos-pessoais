import os
from uuid import uuid4
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]


async def salvar_imagem(foto: UploadFile):

    extensao = foto.filename.split(".")[-1].lower()

    if extensao not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Formato de imagem inválido"
        )

    nome_arquivo = f"{uuid4()}.{extensao}"

    caminho_arquivo = os.path.join(
        UPLOAD_DIR,
        nome_arquivo
    )

    with open(caminho_arquivo, "wb") as buffer:
        buffer.write(await foto.read())

    return f"http://localhost:8000/uploads/{nome_arquivo}"