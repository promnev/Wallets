from rest_framework import serializers

from ..Wallets.models import Wallet
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """This is serializer for TransactionView"""

    class Meta:
        model = Transaction  # models?
        fields = (
            "id",
            "sender",
            "receiver",
            "transfer_amount",
            "commission",
            "status",
            "timestamp",
        )
        read_only_fields = (
            "id",
            "commission",
            "status",
            "timestamp",
        )
