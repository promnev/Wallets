from django.db import models


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    # sender = models.ForeignKey('Wallet', to_field='name', related_name='sender', on_delete=models.PROTECT)
    # receiver = models.ForeignKey('Wallet', to_field='name', related_name='receiver', on_delete=models.PROTECT)
    sender = models.CharField(max_length=20000)
    receiver = models.CharField(max_length=200000)

    transfer_amount = models.DecimalField(max_digits=20, decimal_places=2)
    commission = models.DecimalField(
        max_digits=20, decimal_places=2, default=0
    )
    STATUS = (("PAID", "PAID"), ("FAILED", "FAILED"))
    status = models.CharField(max_length=6, choices=STATUS)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
