# Generated by Django 4.0.6 on 2022-07-27 09:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="receiver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="receiver_name",
                to="payment_app.wallet",
                to_field="name",
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="sender_name",
                to="payment_app.wallet",
                to_field="name",
            ),
        ),
    ]
