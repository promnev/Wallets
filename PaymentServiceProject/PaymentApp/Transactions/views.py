from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response

from ..Wallets.models import Wallet
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionAPIView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        # qs = Wallet.objects.filter(user=self.request.user)
        # qs_wallets_of_cur_user = Wallet.objects.filter(user=self.request.user).values('name')
        # return Transaction.objects.filter(sender__in=Wallet.objects.filter(user=self.request.user).values_list('name', flat=True))
        qs_wallets_of_cur_user = Wallet.objects.filter(
            user=self.request.user
        ).values_list("name", flat=True)
        return Transaction.objects.filter(
            Q(sender__in=qs_wallets_of_cur_user)
            | Q(receiver__in=qs_wallets_of_cur_user)
        )
        # values_list('name', flat=True)

        # return Transaction.objects.filter(Q( self.request.user) | Q(receiver=self.request.user))
        # return Transaction.objects.all()
        # transactions(sender=Wallet.name for cur User)
        # sender=Waller.objects.filter(user=self.request.user).name

    def create(self, request, *args, **kwargs):
        transaction_data = request.data
        new_transaction = Transaction.objects.create(
            sender=Wallet.objects.get(name=transaction_data["sender"]),
            receiver=Wallet.objects.get(name=transaction_data["receiver"]),
            transfer_amount=transaction_data["transfer_amount"],
        )
        new_transaction.save()
        serializer = TransactionSerializer(new_transaction)
        return Response(serializer.data)

    lookup_field = "id"
