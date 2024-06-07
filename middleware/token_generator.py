import jwt
import time
from settings import SECRET_KEY


def generate_token(obj):
    dic = {
        "exp": int(time.time() + 86400),  # 过期时间为一天
        "iat": int(time.time()),
        "id": obj.id,
        "username": obj.username
    }
    return jwt.encode(dic, SECRET_KEY, algorithm="HS256")
