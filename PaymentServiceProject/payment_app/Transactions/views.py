from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.response import Response

from ..Wallets.models import Wallet
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

    def create(self, request, *args, **kwargs) -> Response:
        """Takes in post-request, checks it, creates new transaction and returns its data if all right
        or returns explanation"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    lookup_field = "id"


class TransactionWalletAPIView(viewsets.ModelViewSet):
    """Takes in get-request, returns all transaction where definite wallet is the sender or receiver"""

    serializer_class = TransactionSerializer

    def get_queryset(self, **kwargs):
        return Transaction.objects.filter(
            Q(sender=self.kwargs["wallet_name"])
            | Q(receiver=self.kwargs["wallet_name"])
        )
