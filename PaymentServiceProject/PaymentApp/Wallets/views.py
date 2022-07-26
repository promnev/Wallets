from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Wallet
from .serializers import WalletSerializer


class WalletAPIView(viewsets.ModelViewSet):
    serializer_class = WalletSerializer

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        wallet_data = request.data
        if 0 <= Wallet.objects.filter(user=self.request.user).count() < 5:
            bonus = {"USD": 3.00, "EUR": 3.00, "RUB": 100.00}
            new_wallet = Wallet.objects.create(
                type=wallet_data["type"],
                currency=wallet_data["currency"],
                balance=bonus[f"{wallet_data['currency']}"],
                user=self.request.user,
            )
            new_wallet.save()
            serializer = WalletSerializer(new_wallet)
            return Response(serializer.data)
        else:
            return Response("u can't have more than 5 wallets, bro")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    lookup_field = "name"
