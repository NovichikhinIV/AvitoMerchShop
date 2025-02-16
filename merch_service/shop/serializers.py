from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Product, UserProfile


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = User.objects.filter(username=username).first()

        if user is None:
            user = User.objects.create(
                username=username,
                password=make_password(
                    password
                ),  # Хешируем пароль перед сохранением
            )
            UserProfile.objects.create(user=user)

        return super().validate(attrs)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
