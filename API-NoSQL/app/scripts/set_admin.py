import firebase_admin
from firebase_admin import credentials, auth
import os

Base_Dir = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate(os.path.join(Base_Dir, "..", "serviceAccountKey.json"))
firebase_admin.initialize_app(cred)

uid = input("UID do usuário: ")
auth.set_custom_user_claims(uid, {"role": "admin"})
print("Admin configurado com sucesso")