# Generated by Django 4.0.6 on 2022-07-21 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testapp", "0008_alter_wallet_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="name",
            field=models.CharField(
                default="WsnqWhon", max_length=8, unique=True
            ),
        ),
    ]
