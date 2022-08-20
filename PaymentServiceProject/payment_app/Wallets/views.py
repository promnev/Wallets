from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Wallet
from .serializers import WalletSerializer


class WalletAPIView(viewsets.ModelViewSet):
    """This is the wallet view"""

    serializer_class = WalletSerializer

    def get_queryset(self):
        """Takes in get-request, returns all wallets of current logged-in user"""
        return Wallet.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Takes in post-request, deletes wallet and confirm"""
        instance = self.get_object()
        instance.delete()
        return Response(
            "Wallet deleted successfully", status=status.HTTP_204_NO_CONTENT
        )

    lookup_field = "name"
