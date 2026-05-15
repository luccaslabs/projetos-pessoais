import os
import firebase_admin
from firebase_admin import credentials, firestore

Base_Dir = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate(os.path.join(Base_Dir, "../serviceAccountKey.json"))
firebase_admin.initialize_app(cred)

db = firestore.client()
