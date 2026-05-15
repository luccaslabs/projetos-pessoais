from fastapi import Cookie, HTTPException, Depends
from firebase_admin import auth
from app.services import auth_service

def get_current_user(session: str = Cookie(None)):
    if not session:
        raise HTTPException(status_code=401, detail="Não autenticado")
    try:
        decoded = auth_service.verify_session(session)
        return {
            "uid": decoded["uid"],
            "email": decoded.get("email"),
            "role": decoded.get("role", "user")
        } 
    

    except auth.ExpiredSessionCookieError:
        raise HTTPException(status_code=401, detail="Sessão expirada")
    
    except auth.InvalidSessionCookieError:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao validar sessão")
    
def get_admin_user(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return user