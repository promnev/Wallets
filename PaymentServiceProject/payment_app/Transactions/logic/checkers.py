import environ
from payment_app.Wallets.models import Wallet

env = environ.Env(COMMISSION_VALUE=(float, 0.1))


def trans_amount_validator(transaction_data):
    try:
        trans_amount = float(transaction_data["transfer_amount"])
    except ValueError:
        return False
    if trans_amount < 0:
        return "negative amount"
    return trans_amount


def trans_wallets_checker(transaction_data):
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


def commission_checker(trans_amount, wallets_data):
    commission_amount = trans_amount * env("COMMISSION_VALUE")
    total_amount = trans_amount

    if wallets_data["sender_user"] != wallets_data["receiver_user"]:
        total_amount += commission_amount
    return total_amount
