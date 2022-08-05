from rest_framework import status, viewsets
from rest_framework.response import Response

from .logic.wallet_checkers import user_wallets_count_checker
from .logic.wallet_creating import wallet_creator
from .wallet_models import Wallet
from .wallet_serializers import WalletSerializer


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

        if not user_wallets_count_checker(request_user):
            return Response("You can't have more than 5 wallets")

        new_wallet = wallet_creator(wallet_data, request_user)

        if new_wallet == "type incorrect":
            return Response("Please insert correct type")

        if new_wallet == "currency incorrect":
            return Response("Please insert correct currency")

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
