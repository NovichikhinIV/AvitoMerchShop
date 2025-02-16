from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=1000)  # Начальный баланс

    def __str__(self):
        return f"{self.user.username} - {self.balance} монет"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Transaction(models.Model):
    from_user = models.ForeignKey(
        User, related_name="sent_transactions", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name="received_transactions", on_delete=models.CASCADE
    )
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.from_user} to {self.to_user} - {self.amount} coins"


class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.quantity} items"
