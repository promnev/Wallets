import environ
from payment_app.Wallets.models import Wallet
from rest_framework.response import Response

from PaymentServiceProject.settings import MAX_WALLETS_PER_USER

env = environ.Env()


def if_wallets_limit_was_reached_checker(request_user) -> bool:
    """Takes in request_user, checks the number of his wallets, returns whether the user can create a new wallet"""
    return (
        Wallet.objects.filter(user=request_user).count()
        >= MAX_WALLETS_PER_USER
    )


def wallet_input_checker(wallet_data):
    """Take in wallet_data, check inputs, returns explanation if something wrong"""
    if wallet_data["type"] not in ["Visa", "Mastercard"]:
        return Response("Please insert correct type")

    if wallet_data["currency"] not in ["USD", "EUR", "RUB"]:
        return Response("Please insert correct currency")
