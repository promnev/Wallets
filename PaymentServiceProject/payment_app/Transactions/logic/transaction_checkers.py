from typing import Union

import environ
from payment_app.Wallets.wallet_models import Wallet

env = environ.Env(COMMISSION_VALUE=(float, 0.1))


def trans_amount_validator(transaction_data) -> float:
    """Takes in transaction_data from post-request, checks transaction amount, returns it if all right
    or returns explanation"""
    try:
        trans_amount = float(transaction_data["transfer_amount"])
    except ValueError:
        return False
    except TypeError:
        return "typeerror"
    if trans_amount == 0:
        return "zero"
    if trans_amount < 0:
        return "negative amount"
    return trans_amount


def trans_wallets_checker(transaction_data) -> Union[dict, bool]:
    """Takes in transaction_data from post-request, checks wallet names and access to its data, returns dict with wallets data, it if all right
    or returns explanation"""

    if transaction_data["sender"] not in Wallet.objects.values_list(
        "name", flat=True
    ):
        return "sender incorrect"
    if transaction_data["receiver"] not in Wallet.objects.values_list(
        "name", flat=True
    ):
        return "receiver incorrect"

    try:
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
    except Wallet.DoesNotExist:
        return False
    return {
        "sender_balance": sender_balance,
        "receiver_balance": receiver_balance,
        "sender_currency": sender_currency,
        "receiver_currency": receiver_currency,
        "sender_user": sender_user,
        "receiver_user": receiver_user,
    }


def commission_checker(trans_amount, wallets_data) -> float:
    """Takes in wallet data amd transaction amount, checks if a commission is needed, returns total amount for sender"""

    commission_amount = trans_amount * env("COMMISSION_VALUE")
    total_amount = trans_amount

    if wallets_data["sender_user"] != wallets_data["receiver_user"]:
        total_amount += commission_amount
    return total_amount
