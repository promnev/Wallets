from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.crypto import get_random_string

TYPES = (("Visa", "Visa"), ("Mastercard", "Mastercard"))
CURRENCIES = (("USD", "USD"), ("EUR", "EUR"), ("RUB", "RUB"))


def generate_name() -> str:
    """This is the wallet name generator"""
    return get_random_string(length=8)


class Wallet(models.Model):
    """This is the wallet model"""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=8, unique=True, default=generate_name)

    type = models.CharField(max_length=10, choices=TYPES)
    currency = models.CharField(max_length=3, choices=CURRENCIES)

    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
