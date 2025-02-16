from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import Inventory, Product, UserProfile


class PurchaseItemAPITestCase(APITestCase):
    def setUp(self):
        """Создаем пользователей через API для тестирования перевода монет."""
        self.client.post(
            reverse("token_obtain_pair"),
            {"username": "user1", "password": "password"},
        )
        self.profile = UserProfile.objects.get(user__username="user1")
        self.product = Product.objects.get(name="book")

    def test_buy_item_success(self):
        """Интеграционный тест успешной покупки товара."""
        url = reverse("buy-item", args=[self.product.id])

        response = self.client.post(url)

        self.profile.refresh_from_db()
        inventory_item = Inventory.objects.get(
            user=self.profile.user, product=self.product
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], f"Товар {self.product.name} куплен"
        )
        self.assertEqual(
            self.profile.balance, 950
        )  # Баланс должен уменьшиться на цену товара
        self.assertEqual(
            inventory_item.quantity, 1
        )  # Количество товара в инвентаре увеличилось на 1

    def test_buy_item_not_enough_balance(self):
        """Интеграционный тест покупки товара при недостатке монет."""
        self.profile.balance = 10
        self.profile.save()

        url = reverse("buy-item", args=[self.product.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Недостаточно монет")

    def test_buy_item_non_existent_product(self):
        """Интеграционный тест на покупку товара, которого не существует."""
        non_existent_product_id = 9999  # ID товара, которого нет в базе

        url = reverse("buy-item", args=[non_existent_product_id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], "No Product matches the given query."
        )
