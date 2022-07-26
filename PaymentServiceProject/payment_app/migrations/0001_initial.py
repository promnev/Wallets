# Generated by Django 4.0.6 on 2022-07-26 19:49

import django.core.validators
import django.db.models.deletion
import payment_app.Wallets.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("sender", models.CharField(max_length=20000)),
                ("receiver", models.CharField(max_length=200000)),
                (
                    "transfer_amount",
                    models.DecimalField(decimal_places=2, max_digits=20),
                ),
                (
                    "commission",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=20
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("PAID", "PAID"), ("FAILED", "FAILED")],
                        max_length=6,
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Wallet",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "name",
                    models.CharField(
                        default=payment_app.Wallets.models.generate_name,
                        max_length=8,
                        unique=True,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Visa", "Visa"),
                            ("Mastercard", "Mastercard"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("USD", "USD"),
                            ("EUR", "EUR"),
                            ("RUB", "RUB"),
                        ],
                        max_length=3,
                    ),
                ),
                (
                    "balance",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=20,
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
