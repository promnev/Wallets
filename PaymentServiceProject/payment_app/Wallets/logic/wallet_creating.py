import environ
from django.db import transaction
from payment_app.Wallets.wallet_models import Wallet

env = environ.Env()


@transaction.atomic
def wallet_creator(wallet_data, request_user):
    """Takes in wallet_data from post-request and request_user, checks if the data is correct, creates new wallet and returns its data if all right
    or returns explanation"""

    if wallet_data["type"] not in ["Visa", "Mastercard"]:
        return "type incorrect"
    if wallet_data["currency"] not in ["USD", "EUR", "RUB"]:
        return "currency incorrect"

    bonus = {
        "USD": env("BONUS_FOR_USD"),
        "EUR": env("BONUS_FOR_EUR"),
        "RUB": env("BONUS_FOR_RUB"),
    }
    new_wallet = Wallet.objects.create(
        type=wallet_data["type"],
        currency=wallet_data["currency"],
        balance=bonus[f"{wallet_data['currency']}"],
        user=request_user,
    )
    new_wallet.save()
    return new_wallet
