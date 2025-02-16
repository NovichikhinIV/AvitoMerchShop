from django.urls import path

from .views import (
    BuyItemView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutView,
    ProductListView,
    SendCoinsView,
    UserInfoView,
)


urlpatterns = [
    path(
        "auth/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "auth/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"
    ),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("sendCoin/", SendCoinsView.as_view(), name="send-coin"),
    path("buy/<int:item_id>/", BuyItemView.as_view(), name="buy-item"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("info/", UserInfoView.as_view(), name="user-info"),
]
