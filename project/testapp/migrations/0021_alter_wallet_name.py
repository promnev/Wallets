# Generated by Django 4.0.6 on 2022-07-22 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testapp", "0020_alter_wallet_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="name",
            field=models.CharField(
                default="PRw88LAo", max_length=8, unique=True
            ),
        ),
    ]
