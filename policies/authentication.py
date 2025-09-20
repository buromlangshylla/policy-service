from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import jwt
from decouple import config
from rest_framework_simplejwt.authentication import JWTAuthentication

SERVICE_CLIENT_TOKEN = config("SERVICE_CLIENT_TOKEN")


class ServiceTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("X-Service-Token")
        if token and token == SERVICE_CLIENT_TOKEN:
            return (None, None)
        return None


class ExternalJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                config("JWT_SECRET_KEY"),
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")

        request.jwt_payload = payload
        return (None, None)