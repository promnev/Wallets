from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response

from ..Wallets.models import Wallet
from .logic.checkers import (commission_checker, get_wallet_data_from_db,
                             if_transaction_avalibale_checker,
                             trans_amount_validator,
                             transaction_wallets_input_checker)
from .logic.creating import failed_transaction_creator, transaction_creator
from .models import Transaction
from .serializers import TransactionSerializer


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
        request_user = self.request.user

        if trans_amount_validator(transaction_data):
            return trans_amount_validator(transaction_data)

        if transaction_wallets_input_checker(transaction_data):
            return transaction_wallets_input_checker(transaction_data)

        trans_amount = float(transaction_data["transfer_amount"])

        wallets_data = get_wallet_data_from_db(transaction_data)

        total_amount = commission_checker(trans_amount, wallets_data)

        if if_transaction_avalibale_checker(
            transaction_data,
            trans_amount,
            total_amount,
            wallets_data,
            request_user,
        ):
            return if_transaction_avalibale_checker(
                transaction_data,
                trans_amount,
                total_amount,
                wallets_data,
                request_user,
            )

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
