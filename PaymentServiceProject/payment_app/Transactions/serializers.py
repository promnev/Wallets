from django.db import transaction
from payment_app.Transactions.utils import (commission_checker,
                                            failed_transaction_creator)
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from ..Wallets.models import Wallet
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """This is serializer for TransactionView"""

    sender = serializers.CharField(max_length=8)
    receiver = serializers.CharField(max_length=8)
    transfer_amount = serializers.DecimalField(
        max_digits=20, decimal_places=2, min_value=0.01
    )

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

    def validate(self, data):
        """Takes in transaction_request_data, check it, returns error or validated data"""
        request_user = self.context["request"].user
        trans_amount = round(float(data["transfer_amount"]), 2)

        if not Wallet.objects.filter(name=data["sender"]).exists():
            raise ValidationError("Please insert correct sender wallet name")
        elif not Wallet.objects.filter(name=data["receiver"]).exists():
            raise ValidationError("Please insert correct receiver wallet name")

        obj_sender = Wallet.objects.get(name=data["sender"])
        obj_receiver = Wallet.objects.get(name=data["receiver"])
        total_amount = commission_checker(
            trans_amount, obj_sender, obj_receiver
        )

        if obj_sender.user != request_user:
            raise ValidationError(
                "Wallet access is not allowed. Check if you typed your wallet name correctly."
            )
        elif obj_sender.currency != obj_receiver.currency:
            raise ValidationError(
                "You can't send money to a wallet with a different currency"
            )
        elif obj_sender.balance < total_amount:
            failed_transaction_creator(data, total_amount, trans_amount)
            raise ValidationError(
                "You haven't enough money for this transaction"
            )
        return data

    @transaction.atomic
    def create(self, validated_data):
        """Takes in validated_data, creates new transaction and returns its data"""

        trans_amount = round(float(validated_data["transfer_amount"]), 2)

        obj_sender = Wallet.objects.get(name=validated_data["sender"])
        obj_receiver = Wallet.objects.get(name=validated_data["receiver"])

        total_amount = commission_checker(
            trans_amount, obj_sender, obj_receiver
        )

        obj_sender.balance = float(obj_sender.balance) - total_amount
        obj_sender.save()

        obj_receiver.balance = float(obj_receiver.balance) + trans_amount
        obj_receiver.save()

        new_transaction = Transaction.objects.create(
            sender=obj_sender,
            receiver=obj_receiver,
            transfer_amount=validated_data["transfer_amount"],
            commission=(total_amount - trans_amount),
            status="PAID",
        )
        return new_transaction
