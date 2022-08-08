from typing import Union

import environ
from payment_app.Transactions.logic.creating import failed_transaction_creator
from payment_app.Wallets.models import Wallet
from rest_framework.response import Response

from PaymentServiceProject.settings import COMMISSION_VALUE

env = environ.Env(COMMISSION_VALUE=(float, 0.1))


def trans_amount_validator(transaction_data) -> float:
    """Takes in transaction_data from post-request, checks transaction amount, and returns explanation
    if something wrong"""
    try:
        trans_amount = float(transaction_data["transfer_amount"])
    except ValueError:
        return Response(
            "Please insert only numbers in transaction amount field"
        )
    except TypeError:
        return Response("Please insert transaction amount")
    if trans_amount == 0:
        return Response("Please insert positive transaction amount")
    if trans_amount < 0:
        return Response("You cannot send a negative amount")


def transaction_wallets_input_checker(transaction_data):
    if transaction_data["sender"] not in Wallet.objects.values_list(
        "name", flat=True
    ):
        return Response("Please insert correct sender wallet name")

    if transaction_data["receiver"] not in Wallet.objects.values_list(
        "name", flat=True
    ):
        return Response("Please insert correct receiver wallet name")


def if_transaction_avalibale_checker(
    transaction_data, trans_amount, total_amount, wallets_data, request_user
):
    """Takes in transaction_data from post-request, checks wallet names and access to its data, returns dict with wallets data, it if all right
    or returns explanation"""

    if wallets_data["sender_user"] != request_user:
        return Response(
            "Wallet access is not allowed. Check if you typed your wallet name correctly."
        )

    if wallets_data["sender_currency"] != wallets_data["receiver_currency"]:
        return Response(
            "You can't send money to a wallet with a different currency"
        )

    if wallets_data["sender_balance"] < total_amount:
        failed_transaction_creator(
            transaction_data, total_amount, trans_amount
        )
        return Response("You haven't enough money for this transaction")


def commission_checker(trans_amount, wallets_data) -> float:
    """Takes in wallet data amd transaction amount, checks if a commission is needed, returns total amount for sender"""

    commission_amount = trans_amount * COMMISSION_VALUE
    total_amount = trans_amount

    if wallets_data["sender_user"] != wallets_data["receiver_user"]:
        total_amount += commission_amount
    return total_amount


def get_wallet_data_from_db(transaction_data) -> Union[dict, bool]:
    sender_balance = float(
        getattr(
            Wallet.objects.get(name=transaction_data["sender"]),
            "balance",
        )
    )
    receiver_balance = float(
        getattr(
            Wallet.objects.get(name=transaction_data["receiver"]),
            "balance",
        )
    )
    sender_currency = getattr(
        Wallet.objects.get(name=transaction_data["sender"]), "currency"
    )
    receiver_currency = getattr(
        Wallet.objects.get(name=transaction_data["receiver"]),
        "currency",
    )

    sender_user = getattr(
        Wallet.objects.get(name=transaction_data["sender"]), "user"
    )
    receiver_user = getattr(
        Wallet.objects.get(name=transaction_data["receiver"]), "user"
    )

    return {
        "sender_balance": sender_balance,
        "receiver_balance": receiver_balance,
        "sender_currency": sender_currency,
        "receiver_currency": receiver_currency,
        "sender_user": sender_user,
        "receiver_user": receiver_user,
    }
