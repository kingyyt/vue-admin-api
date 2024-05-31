import jwt
import datetime 
from django.conf import settings

def create_token(payload,timeout=60):
    # 构造header
    headers = {
        "typ": "JWT",
        "alg": "HS256"
    }
    # 构造payload
    payload = {
        # 'user_id':instance.id,
        # "username": instance.username,
        "exp":datetime.datetime.utcnow() + datetime.timedelta(seconds=timeout),
    }

    token = jwt.encode(payload=payload,key=settings.SECRET_KEY,algorithm="HS256",headers=headers).decode("utf-8")
    return token