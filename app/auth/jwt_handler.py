# fungsi yang dibuat dalam file ini bertugas untuk signing, encoding, decoding lalu mereturn jwt
import time
import jwt
from decouple import config

JWT_SECRET = config("SECRET")
JWT_ALGORITHM = config("ALGORITHM")


def token_response(token: str):
    return {
        "status_code": 200,
        "access_token": token
    }


def signJWT(userID: str, username : str, email : str, phone :str):
    payload = {
        "userID": userID,
        "nama" :username,
        "email" : email,
        "phone" : phone,
        "expire": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token if decode_token['expire'] >= time.time() else None
    except:
        return {"Status" : "Token Tidak Valid!"}
