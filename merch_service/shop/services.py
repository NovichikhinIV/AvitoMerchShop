from django.contrib.auth.models import User
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Inventory, Product, Transaction, UserProfile


class TransactionService:
    """Сервис для переводов монет"""

    @staticmethod
    def send_coins(from_user, to_username, amount):
        if amount <= 0:
            return {"error": "Некорректная сумма"}, 400

        try:
            with transaction.atomic():
                to_user = get_object_or_404(User, username=to_username)

                if from_user == to_user:
                    return {
                        "error": "Невозможно перевести монеты самому себе"
                    }, 400

                from_profile = get_object_or_404(UserProfile, user=from_user)
                to_profile = get_object_or_404(UserProfile, user=to_user)

                if from_profile.balance < amount:
                    return {"error": "Недостаточно монет"}, 400

                from_profile.balance -= amount
                to_profile.balance += amount
                from_profile.save()
                to_profile.save()

                Transaction.objects.create(
                    from_user=from_user, to_user=to_user, amount=amount
                )

                return {"message": "Перевод успешно выполнен"}, 200

        except Http404:
            return {"error": "Пользователь не найден"}, 404
        except Exception as e:
            return {"error": str(e)}, 500


class PurchaseService:
    """Сервис для покупки товаров"""

    @staticmethod
    def buy_item(user, item_id):
        product = get_object_or_404(Product, id=item_id)
        profile = get_object_or_404(UserProfile, user=user)

        if profile.balance < product.price:
            return {"error": "Недостаточно монет"}, 400

        try:
            with transaction.atomic():
                profile.balance -= product.price
                profile.save()

                inventory_item, created = Inventory.objects.get_or_create(
                    user=user, product=product
                )
                inventory_item.quantity += 1
                inventory_item.save()

            return {"message": f"Товар {product.name} куплен"}, 200

        except Exception as e:
            return {"error": f"Ошибка при покупке: {str(e)}"}, 500


def get_user_info(user):
    user_profile = UserProfile.objects.get(user=user)
    coins = user_profile.balance

    inventory = [
        {"type": item.product.name, "quantity": item.quantity}
        for item in Inventory.objects.filter(user=user)
    ]

    sent = [
        {"toUser": trans.to_user.username, "amount": trans.amount}
        for trans in Transaction.objects.filter(from_user=user)
    ]

    received = [
        {"fromUser": trans.from_user.username, "amount": trans.amount}
        for trans in Transaction.objects.filter(to_user=user)
    ]

    return {
        "coins": coins,
        "inventory": inventory,
        "coinHistory": {
            "received": received,
            "sent": sent,
        },
    }
