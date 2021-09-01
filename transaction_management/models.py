from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from asset_management.models import UserAsset


class Transaction(models.Model):
    amount = models.FloatField()
    price = models.FloatField()
    fee = models.FloatField()
    date = models.DateField()
    date_time_add = models.DateTimeField(auto_now_add=True)

    @property
    def volume(self):
        return self.amount * self.price

    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 8)
        self.price = round(self.price, 4)
        super(Transaction, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date', '-date_time_add']


class Buy(Transaction):
    user_asset = models.ForeignKey(UserAsset, on_delete=models.CASCADE, related_name="buys")

    def __str__(self):
        return f"{self.user_asset.user.username} - {self.user_asset.asset.symbol} - {self.amount}"

    @property
    def fee_amount(self):
        return (self.amount * self.fee) / 100

    @property
    def net_amount(self):
        return self.amount - self.fee_amount


class Sell(Transaction):
    user_asset = models.ForeignKey(UserAsset, on_delete=models.CASCADE, related_name="sells")

    def __str__(self):
        return f"{self.user_asset.user.username} - {self.user_asset.asset.symbol} - {self.amount}"

    @property
    def fee_amount(self):
        return (self.volume * self.fee) / 100

    @property
    def net_volume(self):
        return self.volume - self.fee_amount
