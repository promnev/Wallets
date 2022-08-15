from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from PaymentServiceProject.settings import (BONUS_FOR_EUR, BONUS_FOR_RUB,
                                            BONUS_FOR_USD,
                                            MAX_WALLETS_PER_USER)

from .models import CURRENCIES, TYPES, Wallet


class WalletSerializer(serializers.ModelSerializer):
    """This is the wallet serializer"""

    type = serializers.ChoiceField(choices=TYPES)
    currency = serializers.ChoiceField(choices=CURRENCIES)

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

    def validate(self, data):
        """Takes in request_user, checks the number of his wallets, returns whether the user can create a new wallet"""
        request_user = self.context["request"].user
        if (
            Wallet.objects.filter(user=request_user).count()
            >= MAX_WALLETS_PER_USER
        ):
            raise ValidationError(
                f"You can't have more than {MAX_WALLETS_PER_USER} wallets"
            )
        return data

    @transaction.atomic
    def create(self, validated_data):
        """Takes in validated_data, creates new wallet and returns its data"""
        bonus = {
            "USD": BONUS_FOR_USD,
            "EUR": BONUS_FOR_EUR,
            "RUB": BONUS_FOR_RUB,
        }

        new_wallet = Wallet.objects.create(
            type=validated_data["type"],
            currency=validated_data["currency"],
            balance=bonus[f"{validated_data['currency']}"],
            user=self.context["request"].user,
        )
        return new_wallet
