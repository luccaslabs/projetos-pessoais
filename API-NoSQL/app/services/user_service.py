from app.external_services.firebase import db

def create_user(uid: str, nome: str, email: str):
    db.collection("usuarios").document(uid).set({
        "nome": nome,
        "email": email
    })