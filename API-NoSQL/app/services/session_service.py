from firebase_admin import auth

def create_session(token: str):
    expires = 60*60*24*5
    session_cookie = auth.create_session_cookie(token, expires_in=expires)
    return session_cookie, expires