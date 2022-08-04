from rest_framework import status, viewsets
from rest_framework.response import Response

from .logic.checkers import user_wallets_count_checker
from .logic.wallet_creating import wallet_creator
from .models import Wallet
from .serializers import WalletSerializer


class WalletAPIView(viewsets.ModelViewSet):
    serializer_class = WalletSerializer

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        wallet_data = request.data
        request_user = self.request.user

        if not user_wallets_count_checker(request_user):
            return Response("You can't have more than 5 wallets")

        new_wallet = wallet_creator(wallet_data, request_user)

        if not new_wallet:
            return Response("Please insert correct type and currency")

        serializer = WalletSerializer(new_wallet)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    lookup_field = "name"
