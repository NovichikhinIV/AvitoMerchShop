from django.contrib.auth.models import User
from django.http.response import Http404
from django.test import TestCase

from shop.models import Inventory, Product, Transaction, UserProfile
from shop.services import PurchaseService, TransactionService, get_user_info


class TransactionServiceTestCase(TestCase):
    def setUp(self):
        """Создаем тестовых пользователей и профили."""
        self.user1 = User.objects.create_user(
            username="user1", password="password"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="password"
        )

        self.profile1 = UserProfile.objects.create(user=self.user1, balance=100)
        self.profile2 = UserProfile.objects.create(user=self.user2, balance=50)

    def test_send_coins_success(self):
        """Тест успешного перевода монет"""
        response, status = TransactionService.send_coins(
            self.user1, "user2", 30
        )

        self.profile1.refresh_from_db()
        self.profile2.refresh_from_db()

        self.assertEqual(status, 200)
        self.assertEqual(response["message"], "Перевод успешно выполнен")
        self.assertEqual(self.profile1.balance, 70)
        self.assertEqual(self.profile2.balance, 80)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_send_coins_not_enough_balance(self):
        """Тест перевода при нехватке монет"""
        response, status = TransactionService.send_coins(
            self.user1, "user2", 150
        )

        self.assertEqual(status, 400)
        self.assertEqual(response["error"], "Недостаточно монет")

    def test_send_coins_invalid_amount(self):
        """Тест перевода с некорректной суммой"""
        response, status = TransactionService.send_coins(
            self.user1, "user2", -10
        )

        self.assertEqual(status, 400)
        self.assertEqual(response["error"], "Некорректная сумма")

    def test_send_coins_self_transfer(self):
        """Тест на ситуацию, когда пользователь пытается передать монеты самому себе"""
        response, status = TransactionService.send_coins(
            self.user1, "user1", 50
        )

        self.assertEqual(status, 400)
        self.assertEqual(
            response["error"], "Невозможно перевести монеты самому себе"
        )


class PurchaseServiceTestCase(TestCase):
    def setUp(self):
        """Создаем тестового пользователя и товар."""
        self.user = User.objects.create_user(
            username="buyer", password="password"
        )
        self.profile = UserProfile.objects.create(user=self.user, balance=100)
        self.product = Product.objects.get(name="book")

    def test_buy_item_success(self):
        """Тест успешной покупки товара"""
        response, status = PurchaseService.buy_item(self.user, self.product.id)

        self.profile.refresh_from_db()
        inventory_item = Inventory.objects.get(
            user=self.user, product=self.product
        )

        self.assertEqual(status, 200)
        self.assertEqual(
            response["message"], f"Товар {self.product.name} куплен"
        )
        self.assertEqual(self.profile.balance, 50)
        self.assertEqual(inventory_item.quantity, 1)

    def test_buy_item_not_enough_balance(self):
        """Тест покупки при нехватке монет"""
        self.profile.balance = 10
        self.profile.save()

        response, status = PurchaseService.buy_item(self.user, self.product.id)

        self.assertEqual(status, 400)
        self.assertEqual(response["error"], "Недостаточно монет")

    def test_buy_item_inventory_increase(self):
        """Тест увеличения количества товара в инвентаре при повторной покупке"""
        # Покупаем товар дважды
        PurchaseService.buy_item(self.user, self.product.id)
        response, status = PurchaseService.buy_item(self.user, self.product.id)

        inventory_item = Inventory.objects.get(
            user=self.user, product=self.product
        )

        self.assertEqual(status, 200)
        self.assertEqual(
            response["message"], f"Товар {self.product.name} куплен"
        )
        self.assertEqual(inventory_item.quantity, 2)

    def test_buy_item_non_existent_product(self):
        """Тест на покупку товара, которого не существует"""
        non_existent_product_id = 9999  # ID товара, которого нет в базе

        with self.assertRaises(Http404):
            PurchaseService.buy_item(self.user, non_existent_product_id)


class GetUserInfoTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user, balance=500
        )

        self.product1 = Product.objects.create(name="Product1", price=100)
        self.product2 = Product.objects.create(name="Product2", price=150)
        Inventory.objects.create(
            user=self.user, product=self.product1, quantity=2
        )
        Inventory.objects.create(
            user=self.user, product=self.product2, quantity=1
        )

        # Создаем несколько транзакций
        self.to_user = User.objects.create_user(
            username="otheruser", password="otherpassword"
        )
        self.transaction1 = Transaction.objects.create(
            from_user=self.user, to_user=self.to_user, amount=50
        )
        self.transaction2 = Transaction.objects.create(
            from_user=self.user, to_user=self.to_user, amount=100
        )

    def test_get_user_info(self):
        user_info = get_user_info(self.user)

        # Проверяем, что в ответе есть баланс
        self.assertIn("coins", user_info)
        self.assertEqual(user_info["coins"], 500)  # Баланс пользователя

        # Проверяем, что в инвентаре два товара
        self.assertIn("inventory", user_info)
        self.assertEqual(
            len(user_info["inventory"]), 2
        )  # Два товара в инвентаре
        self.assertEqual(user_info["inventory"][0]["type"], "Product1")
        self.assertEqual(user_info["inventory"][0]["quantity"], 2)
        self.assertEqual(user_info["inventory"][1]["type"], "Product2")
        self.assertEqual(user_info["inventory"][1]["quantity"], 1)

        # Проверяем историю транзакций
        self.assertIn("coinHistory", user_info)
        self.assertIn("sent", user_info["coinHistory"])
        self.assertEqual(
            len(user_info["coinHistory"]["sent"]), 2
        )  # Две транзакции отправлены
        self.assertEqual(
            user_info["coinHistory"]["sent"][0]["toUser"], "otheruser"
        )
        self.assertEqual(user_info["coinHistory"]["sent"][0]["amount"], 50)

        self.assertIn("received", user_info["coinHistory"])
        self.assertEqual(
            len(user_info["coinHistory"]["received"]), 0
        )  # Пока не получено монет
