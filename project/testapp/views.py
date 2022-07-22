from rest_framework import generics, viewsets

from .models import Transaction, Wallet
from .serializers import TransactionSerializer, WalletSerializer


class WalletAPIview(generics.ListCreateAPIView):
    """Apiview for Wallets."""

    serializer_class = WalletSerializer

    def get_queryset(self):
        """This function returns to user all his wallets."""
        cur_user = self.request.user
        return Wallet.objects.filter(user=cur_user)


class TransactionAPIview(generics.ListCreateAPIView):
    """Apiview for user's transactions"""

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class WalletsOfCurUser(viewsets.ModelViewSet):
    """Apiview for certain wallet"""

    serializer_class = WalletSerializer

    def get_queryset(self):
        """This function returns to user certain wallet, defined in request"""
        cur_user = self.request.user
        return Wallet.objects.filter(user=cur_user)

    lookup_field = "name"
