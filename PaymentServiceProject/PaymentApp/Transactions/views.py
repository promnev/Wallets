from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response

from ..Wallets.models import Wallet
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionAPIView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        # return Transaction.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))
        return Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        transaction_data = request.data
        new_transaction = Transaction.objects.create(
            sender=Wallet.user,
            receiver=Wallet.user,
            transfer_amount=transaction_data["transfer_amount"],
        )
        new_transaction.save()
        serializer = TransactionSerializer(new_transaction)
        return Response(serializer.data)

    # lookup_field = "id"
