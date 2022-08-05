from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response

from ..Wallets.wallet_models import Wallet
from .logic.transaction_checkers import (commission_checker,
                                         trans_amount_validator,
                                         trans_wallets_checker)
from .logic.transaction_creating import (failed_transaction_creator,
                                         transaction_creator)
from .transaction_models import Transaction
from .transaction_serializers import TransactionSerializer


class TransactionAPIView(viewsets.ModelViewSet):
    """This is the transaction view"""

    serializer_class = TransactionSerializer

    def get_queryset(self):
        """Takes in get-request, returns all transaction where current logged-in user is the sender or receiver"""
        qs_wallets_of_cur_user = Wallet.objects.filter(
            user=self.request.user
        ).values_list("name", flat=True)
        return Transaction.objects.filter(
            Q(sender__in=qs_wallets_of_cur_user)
            | Q(receiver__in=qs_wallets_of_cur_user)
        )

    def create(self, request, *args, **kwargs):
        """Takes in post-request, checks it, creates new transaction and returns its data if all right
        or returns explanation"""
        transaction_data = request.data

        trans_amount = trans_amount_validator(transaction_data)
        if trans_amount == "typeerror":
            return Response("Please insert transaction amount")

        if trans_amount == "zero":
            return Response("Please insert positive transaction amount")

        if not trans_amount:
            return Response(
                "Please insert only numbers in transaction amount field"
            )
        if trans_amount == "negative amount":
            return Response("You cannot send a negative amount")

        wallets_data = trans_wallets_checker(transaction_data)

        if wallets_data == "sender incorrect":
            return Response("Please insert correct sender wallet name")

        if wallets_data == "receiver incorrect":
            return Response("Please insert correct receiver wallet name")

        if not wallets_data:
            return Response("Something go wrong")

        if wallets_data["sender_user"] != self.request.user:
            return Response(
                "Wallet access is not allowed. Check if you typed your wallet name correctly."
            )

        if (
            wallets_data["sender_currency"]
            != wallets_data["receiver_currency"]
        ):
            return Response(
                "You can't send money to a wallet with a different currency"
            )

        total_amount = commission_checker(trans_amount, wallets_data)

        if wallets_data["sender_balance"] < total_amount:
            failed_transaction_creator(
                transaction_data, total_amount, trans_amount
            )
            return Response("You haven't enough money for this transaction")

        new_transaction = transaction_creator(
            transaction_data, wallets_data, total_amount, trans_amount
        )

        if not new_transaction:
            failed_transaction_creator(
                transaction_data, total_amount, trans_amount
            )
            return Response("Transaction failed")

        serializer = TransactionSerializer(new_transaction)
        return Response(serializer.data)

    lookup_field = "id"


class TransactionWalletAPIView(viewsets.ModelViewSet):
    """Takes in get-request, returns all transaction where definite wallet is the sender or receiver"""

    serializer_class = TransactionSerializer

    def get_queryset(self, **kwargs):
        return Transaction.objects.filter(
            Q(sender=self.kwargs["wallet_name"])
            | Q(receiver=self.kwargs["wallet_name"])
        )
