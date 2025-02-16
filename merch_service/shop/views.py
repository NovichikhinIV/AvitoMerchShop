from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Product
from .serializers import CustomTokenObtainPairSerializer, ProductSerializer
from .services import PurchaseService, TransactionService, get_user_info


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get("access")
        refresh_token = response.data.get("refresh")

        # Сохраняем access-токен в HttpOnly cookie
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=access_token,
            httponly=True,
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )

        # Сохраняем refresh-токен в HttpOnly cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Берем refresh-токен из куков
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"error": "No refresh token"}, status=400)

        # Создаем новый запрос с refresh-токеном
        request.data["refresh"] = refresh_token
        response = super().post(request, *args, **kwargs)

        access_token = response.data.get("access")
        if access_token:
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
        return response


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response = Response({"message": "Logged out successfully"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class SendCoinsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        from_user = request.user
        to_username = request.data.get("toUser")
        amount = int(request.data.get("amount", 0))
        response, status_code = TransactionService.send_coins(
            from_user, to_username, amount
        )
        return Response(response, status=status_code)


class BuyItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, item_id):
        response, status_code = PurchaseService.buy_item(request.user, item_id)
        return Response(response, status=status_code)


class ProductListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_info = get_user_info(user)
        return Response(user_info)
