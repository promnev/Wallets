from rest_framework import status, viewsets
from rest_framework.response import Response

from PaymentServiceProject.settings import MAX_WALLETS_PER_USER

from .logic.checkers import (if_wallets_limit_was_reached_checker,
                             wallet_input_checker)
from .logic.creating import wallet_creator
from .models import Wallet
from .serializers import WalletSerializer


class WalletAPIView(viewsets.ModelViewSet):
    """This is the wallet view"""

    serializer_class = WalletSerializer

    def get_queryset(self):
        """Takes in get-request, returns all wallets of current logged-in user"""
        return Wallet.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Takes in post-request, checks it, creates new wallet and returns its data if all right
        or returns explanation"""
        wallet_data = request.data
        request_user = self.request.user

        if if_wallets_limit_was_reached_checker(request_user):
            return Response(
                f"You can't have more than {MAX_WALLETS_PER_USER} wallets"
            )

        if wallet_input_checker(wallet_data):
            return wallet_input_checker(wallet_data)

        new_wallet = wallet_creator(wallet_data, request_user)

        serializer = WalletSerializer(new_wallet)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Takes in post-request, deletes wallet and confirm"""
        instance = self.get_object()
        instance.delete()
        return Response(
            "Wallet deleted successfully", status=status.HTTP_204_NO_CONTENT
        )

    lookup_field = "name"
