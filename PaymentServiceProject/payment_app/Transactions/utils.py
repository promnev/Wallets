from payment_app.Transactions.models import Transaction
from payment_app.Wallets.models import Wallet

from PaymentServiceProject.settings import COMMISSION_VALUE


def commission_checker(trans_amount, obj_sender, obj_receiver) -> float:
    """Takes in wallet data amd transaction amount, checks if a commission is needed, returns total amount for sender"""

    commission_amount = trans_amount * COMMISSION_VALUE
    total_amount = trans_amount

    if obj_sender.user != obj_receiver.user:
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


#
