import environ
from django.db import transaction
from payment_app.Wallets.models import Wallet

env = environ.Env()


@transaction.atomic
def wallet_creator(wallet_data, request_user):
    try:
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
    except KeyError:
        return False
    return new_wallet
