from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response

from ..Wallets.models import Wallet
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionAPIView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        qs_wallets_of_cur_user = Wallet.objects.filter(
            user=self.request.user
        ).values_list("name", flat=True)
        return Transaction.objects.filter(
            Q(sender__in=qs_wallets_of_cur_user)
            | Q(receiver__in=qs_wallets_of_cur_user)
        )

    def create(self, request, *args, **kwargs):
        transaction_data = request.data
        trans_amount = float(transaction_data["transfer_amount"])
        sender_balance = float(
            getattr(
                Wallet.objects.get(name=transaction_data["sender"]), "balance"
            )
        )
        receiver_balance = float(
            getattr(
                Wallet.objects.get(name=transaction_data["receiver"]),
                "balance",
            )
        )
        commission_amount = trans_amount / 10
        total_amount = trans_amount
        sender_user = getattr(
            Wallet.objects.get(name=transaction_data["sender"]), "user"
        )
        receiver_user = getattr(
            Wallet.objects.get(name=transaction_data["receiver"]), "user"
        )

        if not sender_user == receiver_user:
            total_amount += commission_amount

        if sender_balance >= total_amount:
            # try:

            obj_sender = Wallet.objects.get(name=transaction_data["sender"])
            obj_sender.balance = sender_balance - total_amount
            obj_sender.save()

            obj_receiver = Wallet.objects.get(
                name=transaction_data["receiver"]
            )
            obj_receiver.balance = receiver_balance + trans_amount
            obj_receiver.save()

            new_transaction = Transaction.objects.create(
                sender=Wallet.objects.get(name=transaction_data["sender"]),
                receiver=Wallet.objects.get(name=transaction_data["receiver"]),
                transfer_amount=transaction_data["transfer_amount"],
                commission=(total_amount - trans_amount),
                status="PAID",
            )
            new_transaction.save()
            serializer = TransactionSerializer(new_transaction)

            # except:
            #     return Response('transaction failed')
            #
            # else:
            return Response(serializer.data)

        else:
            return Response("u haven't enough money for this transaction, bro")

    lookup_field = "id"
