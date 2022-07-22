from rest_framework import serializers

from .models import Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):
    """This is serializer for WalletView"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Wallet
        fields = (
            "name",
            "type",
            "currency",
            "balance",
            "created_on",
            "modified_on",
            "user",
        )
        read_only_fields = (
            "name",
            "balance",
            "created_on",
            "modified_on",
        )


class TransactionSerializer(serializers.ModelSerializer):
    """This is serializer for TransactionView"""

    class Meta:
        model = Transaction
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
