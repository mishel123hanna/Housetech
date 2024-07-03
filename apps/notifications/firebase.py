import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("/home/mishel/Graduation_Project/housetech-401d8-firebase-adminsdk-ucjlm-1a66bacdbe.json")
default_app = firebase_admin.initialize_app(cred)

# 