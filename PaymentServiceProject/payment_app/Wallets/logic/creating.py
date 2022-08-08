import environ
from django.db import transaction
from payment_app.Wallets.models import Wallet

from PaymentServiceProject.settings import (BONUS_FOR_EUR, BONUS_FOR_RUB,
                                            BONUS_FOR_USD)

env = environ.Env()


@transaction.atomic
def wallet_creator(wallet_data, request_user):
    """Takes in wallet_data from post-request and request_user, checks if the data is correct,
    creates new wallet and returns its data"""

    bonus = {
        "USD": BONUS_FOR_USD,
        "EUR": BONUS_FOR_EUR,
        "RUB": BONUS_FOR_RUB,
    }
    new_wallet = Wallet.objects.create(
        type=wallet_data["type"],
        currency=wallet_data["currency"],
        balance=bonus[f"{wallet_data['currency']}"],
        user=request_user,
    )
    new_wallet.save()
    return new_wallet
