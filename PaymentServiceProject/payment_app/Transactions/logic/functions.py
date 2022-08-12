from payment_app.Transactions.models import Transaction
from payment_app.Wallets.models import Wallet

from PaymentServiceProject.settings import COMMISSION_VALUE


def commission_checker(trans_amount, wallets_data) -> float:
    """Takes in wallet data amd transaction amount, checks if a commission is needed, returns total amount for sender"""

    commission_amount = trans_amount * COMMISSION_VALUE
    total_amount = trans_amount

    if wallets_data["sender_user"] != wallets_data["receiver_user"]:
        total_amount += commission_amount
    return total_amount


def failed_transaction_creator(transaction_data, total_amount, trans_amount):
    """Takes in wallet_data, transaction amount and total_amount_user, creates new failed transaction"""
    new_transaction = Transaction.objects.create(
        sender=Wallet.objects.get(name=transaction_data["sender"]),
        receiver=Wallet.objects.get(name=transaction_data["receiver"]),
        transfer_amount=transaction_data["transfer_amount"],
        commission=(total_amount - trans_amount),
        status="FAILED",
    )
    new_transaction.save()


def get_wallet_data_from_db(transaction_data) -> dict:
    """Takes in transaction_data and returns dict with wallet's data for sender and receiver"""
    sender_data = Wallet.objects.get(name=transaction_data["sender"])
    receiver_data = Wallet.objects.get(name=transaction_data["receiver"])

    sender_user = getattr(sender_data, "user")

    sender_balance = float(
        getattr(
            sender_data,
            "balance",
        )
    )

    sender_currency = getattr(sender_data, "currency")

    receiver_user = getattr(receiver_data, "user")

    receiver_balance = float(
        getattr(
            receiver_data,
            "balance",
        )
    )

    receiver_currency = getattr(
        receiver_data,
        "currency",
    )

    return {
        "sender_balance": sender_balance,
        "receiver_balance": receiver_balance,
        "sender_currency": sender_currency,
        "receiver_currency": receiver_currency,
        "sender_user": sender_user,
        "receiver_user": receiver_user,
    }
