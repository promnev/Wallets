from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string


class Wallet(models.Model):
    """Model for wallet"""

    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=8, unique=True, default=get_random_string(length=8)
    )
    TYPE = (("Visa", "Visa"), ("Mastercard", "Mastercard"))
    CUR = (("USD", "USD"), ("EUR", "EUR"), ("RUB", "RUB"))
    type = models.CharField(max_length=10, choices=TYPE)
    currency = models.CharField(max_length=3, choices=CUR)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        """This function returns name of Wallets"""
        return self.name


class Transaction(models.Model):
    """Model for Transaction"""

    id = models.AutoField(primary_key=True)
    sender = models.CharField
    receiver = models.CharField
    transfer_amount = models.DecimalField(
        max_digits=20, decimal_places=2, default=0
    )
    commission = models.DecimalField(
        max_digits=20, decimal_places=2, default=0
    )
    STATUS = (("PAID", "PAID"), ("FAILED", "FAILED"))
    status = models.CharField(max_length=6, choices=STATUS)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """This function returns id of Transaction"""
        return self.id
