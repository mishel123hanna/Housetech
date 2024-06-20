# from google.auth.transport.requests import Request
# from google.oauth2 import service_account
# import requests
# import json

# # We are generating an access_token to be used whenever we want to make a request to FCM
# def generate_firebase_auth_key():
#     scopes = ['https://www.googleapis.com/auth/firebase.messaging']
    
    
#     # Replace the value of credentials_info with what you downloaded from Firebase cloud messaging
#     credentials_info = {
#         "type": "service_account",
#         "project_id": "**********",
#         "private_key_id": "**********************",
#         "private_key": "-----BEGIN PRIVATE KEY-----\*******IBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCslg97SnS0HXAI\nLLQK+yLZ9xYXhVKbSa3B+67IZIi6dRtF0+hAGVjDCDCpfLWQd/lRgu8FO1zQVWT6\nMlyMVSkipOuqPUzlfTO6/gJBOZLzV2SrX4s7GC9nIHY07qLXgUl4m2eAk6XNyGac\nxm34/NN26Ne70i4WpYpCzdDaUAksWoidJnnyE1aQ1CJC+plwZHv1/yZ6nqxJIm34\nza0abvMvi6Jf0SHXLVPdZrtJVMGub74XJzF8VZLVQ9Tb9GRNZ5MWa1dNeyIM5pru\nhYnR6MRpLoYXjHxZCzOl8kX9eg5DAHtSA0JwCo6dxsbYbGAKEKuyrxXeKFxeSU0L\nUcnHr38bAgMBAAECggEAE0Bn+LJNA1x3R0opSUJLWHICAlyqYs0ct1NKY2snf1kZ\n0je5pBDPwG208+sH29YuNwP6gqRlDY5BBdHBVhwXyxgHe8V7wuus7hJwkPMJq+BX\nR/CP+OcRPpk15mCqRIzU88GuEX8m0yYkIB/YW5pkQlLl4bsnzfnoStxnjDq6UzqU\n5x/kUQE2g8Lq9k7y49gfIKIk6HuYmi7m1pzfYkbsPqqh3qVpMA1sefCVbhZY0Y/V\nlE1zOWWeL0XctL9/AiDdoJR8Laa8IqK3EosNtPGhLWWpH1AdAcrTe6Phg9YgWHJw\nLMTJBC1d0hNpp26RdjbJXhLv6E8rPJcU/GWmgRGZHQKBgQDr1PjlgLBVvjWW5K/i\nTlblh8bUunhAw/6vjmW03KSx2iKS1oQXeiAVMnXHi92/SB3TSIPUP8mzBXpZsI9D\nNvAi/GHbOrN3cNfP0w/qLdgh1msiY7qrpUW+XV9bLTdfpXxuy+pDRFKWyBtD9vYE\ndbNujC6jfD9dBJXMzbGnZtfylQKBgQC7WHW8nMFySEhW5zu8+IVrrpdf5LnyyQol\nEh44vVC5WumcZ40YLe5SogJuQzT37rXRqMzOpedophioaLjiNVblqNHL+t2YYx+h\nO+q3J9gKoPOFbQEzeWJq0HLwtNqVl59yQwEauzoc8DkZV248vHgB4xlEPMnLcchR\nCXqQNHhu7wKBgFNWLCo1wppaH+fVok2vb0enJl0QE+SXHg39nPU/rzdmJSeMhJsj\nPekfrr04MMEig9+g1W0QqX8IpYbCPK384PkMBKyK3taLWsgHBq2zS5gRhERfx5xW\nSAIQTt0SamnzObiReJQStbiwt+nZgHBtA15CTUzaYC3HrAP2gBvu3MrNAoGAPcZb\nfEgMGYzwHYe90P/5rpoxW/NlxUK5T6P7xyXVumjZ4zLZ+YEbtq+pMYaDrsVNusZ4\nUiOufHlYZB+z5xNDhhL2qtYbv6XfxiClsqM2v7p20iYxYTHDXAlD/U8FTJJkhx7E\n/HWEIgqsKUkFFo3m3Ghv6mpI+Aaa0O3ZNje3Bo0CgYAIWCM2GSCuFgBwKdPQuqlC\nrcrj4AMdfI7ptQjQrSJg6a7fL965kxWSuQMebT+JNVEIPDP4RTqvJXPEFV6KmPml\nFjCXbMFWK/OJV4XNDHZIXlZ5yDyMbG8DH59DjgXXRUElLlFQ66NcKCDpPHiNru2H\n1jg5QdjyxCpCZgkrzS0gWQ==\n-----END PRIVATE KEY-----\n",
#         "client_email": "firebase-adminsdk-x7rs4@testpush-8c6ea.iam.gserviceaccount.com",
#         "client_id": "**********************",
#         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#         "token_uri": "https://oauth2.googleapis.com/token",
#         "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#         "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-x7rs4%40testpush-8c6ea.iam.gserviceaccount.com",
#         "universe_domain": "googleapis.com"
#      }

#     credentials = service_account.Credentials.from_service_account_info(
#             credentials_info, scopes=scopes
#         )

#     credentials.refresh(Request())

#     access_token = credentials.token
#     return access_token


# #this function takes the auth_token(our access_token) and fcm_token(this will be generated from the client side.) as arguments.
# # You can customize the message to your preference.
# def send_push_notification(auth_token, fcm_token):
#     url = "https://fcm.googleapis.com/v1/projects/testpush-8c6ea/messages:send"

#     payload = json.dumps({
#     "message": {
#         "token": f'{fcm_token}',
#         "notification": {
#         "title": "New blog published!",
#         "body": "Hey, There is a new blog post you might want to check out."
#         },
#         "data": {
#         "key1": "value1",
#         "key2": "value2"
#         }
#     }
#     })
#     headers = {
#     'Content-Type': 'application/json',
#     'Authorization': f'Bearer {auth_token}'
#     }

#     response = requests.request("POST", url, headers=headers, data=pa)
