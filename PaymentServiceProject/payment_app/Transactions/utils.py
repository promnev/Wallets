from payment_app.Transactions.models import Transaction

from PaymentServiceProject.settings import COMMISSION_VALUE


def commission_checker(
    trans_amount: float, sender_user: str, receiver_user: str
) -> float:
    """Takes sender_user name, receiver_user name amd transaction amount, checks if a commission is needed,
    returns total amount for sender"""

    commission_amount = trans_amount * COMMISSION_VALUE
    total_amount = trans_amount

    if sender_user != receiver_user:
        total_amount += commission_amount
    return total_amount


def failed_transaction_creator(
    sender_name: str,
    receiver_name: str,
    trans_amount: float,
    commission: float,
):
    """Takes in sender name, receiver name, transaction amount and commission amount, creates new failed transaction"""
    new_transaction = Transaction.objects.create(
        sender=sender_name,
        receiver=receiver_name,
        transfer_amount=trans_amount,
        commission=commission,
        status="FAILED",
    )
    new_transaction.save()
