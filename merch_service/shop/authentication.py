from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Берем access-токен из cookie
        access_token = request.COOKIES.get("access_token")

        if not access_token:
            return None  # Если нет токена, пользователь не аутентифицирован

        try:
            validated_token = AccessToken(access_token)
        except Exception:
            raise AuthenticationFailed("Invalid or expired token")

        # DRF ожидает кортеж (пользователь, токен), ищем пользователя по ID
        from django.contrib.auth.models import User

        user_id = validated_token.get("user_id")
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

        return (user, validated_token)
