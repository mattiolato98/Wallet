from django.conf import settings
from django.db import models


class Fiat(models.Model):
    cmc_id = models.PositiveIntegerField()
    name = models.CharField(max_length=150)
    sign = models.CharField(max_length=5)
    symbol = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name} - {self.symbol}'


class Tag(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Asset(models.Model):
    cmc_id = models.PositiveIntegerField(unique=True)
    logo = models.URLField()
    name = models.CharField(max_length=150)
    symbol = models.CharField(max_length=20)
    slug = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=150)

    tags = models.ManyToManyField(Tag, related_name="asset_tags")

    def __str__(self):
        return f"{self.symbol} - {self.name}"


class Url(models.Model):
    value = models.URLField()
    description = models.CharField(max_length=150)

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="urls")

    def __str__(self):
        return f"{self.value}"


class UserPortfolio(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="portfolios")

    def __str__(self):
        return self.name

    @property
    def assets_count(self):
        return self.user_assets.count()

    @property
    def assets(self):
        asset_pk_list = [user_asset.asset.pk for user_asset in self.user_assets.all()]
        return Asset.objects.filter(pk__in=asset_pk_list).all()

    @property
    def assets_ids(self):
        return [user_asset.asset.cmc_id for user_asset in self.user_assets.all()]

    @property
    def buy_volume(self):
        return sum(asset.buy_volume for asset in self.user_assets.all())

    @property
    def sell_volume(self):
        return sum(asset.sell_volume for asset in self.user_assets.all())

    @property
    def net_volume(self):
        return self.sell_volume - self.buy_volume

    @property
    def total_positive_balance(self):
        return sum(asset.net_volume for asset in self.user_assets.all() if asset.net_volume > 0)

    @property
    def total_negative_balance(self):
        return sum(abs(asset.net_volume) for asset in self.user_assets.all() if asset.net_volume < 0)

    @property
    def transaction_count(self):
        return sum(asset.transaction_count for asset in self.user_assets.all())


class UserAsset(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="user_relations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="asset_relations")

    portfolio = models.ForeignKey(UserPortfolio, on_delete=models.CASCADE, related_name="user_assets")

    def __str__(self):
        return f"{self.asset.name} - {self.user.username}"

    @property
    def amount(self):
        return self.buy_amount - self.sell_amount

    @property
    def buy_amount(self):
        return sum(transaction.net_amount for transaction in self.buys.all())

    @property
    def sell_amount(self):
        return sum(transaction.amount for transaction in self.sells.all())

    @property
    def buy_volume(self):
        return sum(transaction.volume for transaction in self.buys.all())

    @property
    def sell_volume(self):
        return sum(transaction.net_volume for transaction in self.sells.all())

    @property
    def net_volume(self):
        return self.sell_volume - self.buy_volume

    @property
    def average_buy_price(self):
        return self.buy_volume / self.buy_amount if self.buy_amount != 0 else 0

    @property
    def average_sell_price(self):
        return self.sell_volume / self.sell_amount if self.sell_amount != 0 else 0

    @property
    def average_load_price(self):
        return (self.buy_volume - self.sell_volume) / (self.buy_amount - self.sell_amount) \
            if (self.buy_amount - self.sell_amount) > 0 else 0

    @property
    def transaction_count(self):
        return self.buys.count() + self.sells.count()

    class Meta:
        unique_together = ['asset', 'user']
