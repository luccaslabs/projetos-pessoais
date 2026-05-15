from fastapi import HTTPException
from firebase_admin import auth
import requests
import os


def create_user(email: str, password: str):
    
    return auth.create_user(email=email, password=password)


def verify_token(token: str):
    return auth.verify_id_token(token)

def verify_session(session: str):
    return auth.verify_session_cookie(session, check_revoked=True)

def login(email: str, senha: str):
    api_key = os.getenv("FIREBASE_API_KEY")
    
    response = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}",
                             json={"email": email, "password": senha, "returnSecureToken": True})

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    return response.json()["idToken"]

def logout_user(session: str):
    decoded = verify_session(session)
    uid = decoded["uid"]

    auth.revoke_refresh_tokens(uid)

    return uid