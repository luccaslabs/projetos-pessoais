from fastapi import APIRouter, Body, HTTPException, Header, Response, Cookie
from app.schemas.user import Usuario, Login
from firebase_admin import auth
from app.services import auth_service, user_service, session_service

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/signup")
async def signup(request: Usuario):
    try:
        usuario = auth_service.create_user(
            email=request.email,
            password=request.senha
        )
        user_service.create_user(
            uid=usuario.uid,
            nome=request.nome,
            email=request.email
        )
        return{
            "uid": usuario.uid,
            "mensagem": "Usuário criado com sucesso"
        }
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=400, 
            detail="E-mail já cadastrado"
        )
    except Exception:
        raise HTTPException(
            status_code=500, 
            detail="Erro ao criar usuário"
        )
    
@auth_router.post("/login")
async def login(response: Response, request: Login):
    token = auth_service.login(request.email, request.senha)
    session_cookie, expires = session_service.create_session(token)
    response.set_cookie(key="session", value=session_cookie, httponly=True, secure=False, samesite="Lax", max_age=expires)
    return {"mensagem": "Login realizado com sucesso"}

@auth_router.post("/logout")
async def logout(response: Response, session: str = Cookie(None)):
    if not session:
        raise HTTPException(status_code=401, detail="Sessão não encontrada")
    try:
        auth_service.logout_user(session)

    except auth.InvalidSessionCookieError:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    
    except auth.ExpiredSessionCookieError:
        raise HTTPException(status_code=401, detail="Sessão expirada")

    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao fazer logout")
    
    finally:
        response.delete_cookie(
            key="session",
            secure=False, # teste local
            samesite="Lax"
        )

    return {
        "mensagem": "Logout realizado com sucesso"
    }