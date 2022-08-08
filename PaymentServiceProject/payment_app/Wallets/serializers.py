from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """This is the wallet serializer"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Wallet
        fields = (
            "id",
            "name",
            "type",
            "currency",
            "balance",
            "created_on",
            "modified_on",
            "user",
        )

        read_only_fields = ("name", "balance")
