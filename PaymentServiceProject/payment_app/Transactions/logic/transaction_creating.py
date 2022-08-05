from django.db import transaction
from payment_app.Transactions.transaction_models import Transaction
from payment_app.Wallets.wallet_models import Wallet


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


@transaction.atomic
def transaction_creator(
    transaction_data, wallets_data, total_amount, trans_amount
):
    """Takes in wallet_data, transaction amount and total_amount_user, creates new transaction and returns its data"""

    obj_sender = Wallet.objects.get(name=transaction_data["sender"])
    obj_sender.balance = wallets_data["sender_balance"] - total_amount
    obj_sender.save()

    obj_receiver = Wallet.objects.get(name=transaction_data["receiver"])
    obj_receiver.balance = wallets_data["receiver_balance"] + trans_amount
    obj_receiver.save()

    new_transaction = Transaction.objects.create(
        sender=Wallet.objects.get(name=transaction_data["sender"]),
        receiver=Wallet.objects.get(name=transaction_data["receiver"]),
        transfer_amount=transaction_data["transfer_amount"],
        commission=(total_amount - trans_amount),
        status="PAID",
    )
    new_transaction.save()

    return new_transaction
