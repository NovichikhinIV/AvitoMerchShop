from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from shop.models import UserProfile


class SendCoinsAPITestCase(APITestCase):
    def setUp(self):
        self.client.post(
            reverse("token_obtain_pair"),
            {"username": "user1", "password": "password1"},
        )
        self.profile1 = UserProfile.objects.get(user__username="user1")

        self.user2 = User.objects.create_user(
            username="user2", password="password2"
        )
        self.profile2 = UserProfile.objects.create(user=self.user2)

    def test_send_coins_success(self):
        """Тест успешного перевода монет от одного пользователя к другому."""
        data = {"toUser": "user2", "amount": 30}
        response = self.client.post(reverse("send-coin"), data, format="json")

        self.profile1.refresh_from_db()
        self.profile2.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Перевод успешно выполнен")
        self.assertEqual(self.profile1.balance, 970)
        self.assertEqual(self.profile2.balance, 1030)

    def test_send_coins_not_enough_balance(self):
        """Тест перевода монет с недостаточным балансом."""
        data = {"toUser": "user2", "amount": 1500}
        response = self.client.post(reverse("send-coin"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Недостаточно монет")

    def test_send_coins_self_transfer(self):
        """Тест перевода монет самому себе (должен быть отклонён)."""
        data = {"toUser": "user1", "amount": 30}
        response = self.client.post(reverse("send-coin"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Невозможно перевести монеты самому себе"
        )
