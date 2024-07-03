import firebase_admin
from firebase_admin import credentials
import environ
from pathlib import Path
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
# cred = credentials.Certificate("/home/mishel/Graduation_Project/housetech-401d8-firebase-adminsdk-ucjlm-1a66bacdbe.json")




# Construct the credentials dictionary from environment variables
firebase_credentials_dict = {
    "type": env('FIREBASE_TYPE'),
    "project_id": env('FIREBASE_PROJECT_ID'),
    "private_key_id": env('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": env('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": env('FIREBASE_CLIENT_EMAIL'),
    "client_id": env('FIREBASE_CLIENT_ID'),
    "auth_uri": env('FIREBASE_AUTH_URI'),
    "token_uri": env('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": env('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": env('FIREBASE_CLIENT_X509_CERT_URL'),
    "universe_domain": env('FIREBASE_UNIVERSE_DOMAIN')
}

# Initialize the Firebase app with the credentials dictionary
cred = credentials.Certificate(firebase_credentials_dict)


default_app = firebase_admin.initialize_app(cred)