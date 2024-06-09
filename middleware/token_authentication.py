import jwt
from settings import SECRET_KEY
from middleware.exceptions import UnauthorizedException


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token has expired")
    except jwt.InvalidTokenError:
        raise UnauthorizedException("Invalid token")


def auth_required(handler_func):
    def wrapper(handler, *args, **kwargs):
        auth_header = handler.headers.get("Token")
        if not auth_header:
            raise UnauthorizedException("Authorization header is missing")

        token = auth_header.split(" ")[1]
        payload = verify_token(token)

        handler.user = payload
        return handler_func(handler, *args, **kwargs)

    return wrapper