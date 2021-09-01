from PIL import Image
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from asset_management.models import Asset, Fiat


class PlatformUser(AbstractUser):
    AbstractUser._meta.get_field('email')._unique = True
    is_manager = models.BooleanField(default=False)

    assets = models.ManyToManyField(Asset, related_name="user_assets", through="asset_management.UserAsset")
    fiat = models.ForeignKey(Fiat, on_delete=models.SET_DEFAULT, related_name="user", default=1)

    def __str__(self):
        return self.username

    @property
    def assets_ids(self):
        return [asset.cmc_id for asset in self.assets.all()]

    @property
    def buy_volume(self):
        return sum(asset.buy_volume for asset in self.asset_relations.all())

    @property
    def sell_volume(self):
        return sum(asset.sell_volume for asset in self.asset_relations.all())

    @property
    def net_volume(self):
        return self.sell_volume - self.buy_volume

    @property
    def total_positive_balance(self):
        return sum(asset.net_volume for asset in self.asset_relations.all() if asset.net_volume > 0)

    @property
    def total_negative_balance(self):
        return sum(abs(asset.net_volume) for asset in self.asset_relations.all() if asset.net_volume < 0)

    @property
    def transaction_count(self):
        return sum(asset.transaction_count for asset in self.asset_relations.all())

    @property
    def has_profile(self):
        try:
            assert self.profile
            return True
        except ObjectDoesNotExist:
            return False


class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="profiles/images/%Y/%m/%d",
                                default="profiles/default/default_picture.jpg",
                                blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        """
        Completa il salvataggio modificando l'immagine del profilo in modo da renderla un quadrato.
        Se non è presente nessuna immagine setta quella di default (utile in caso di eliminazione
        dell'immagine in fase di update).
        """
        super().save()
        if self.picture:
            img = Image.open(self.picture.path)
            width, height = img.size

            if width > 300 and height > 300:
                img.thumbnail((width, height))

            if height < width:
                left = (width - height) / 2
                right = (width + height) / 2
                top = 0
                bottom = height
                img = img.crop((left, top, right, bottom))

            elif width < height:
                left = 0
                right = width
                top = 0
                bottom = width
                img = img.crop((left, top, right, bottom))

            if width > 300 and height > 300:
                img.thumbnail((300, 300))

            img.save(self.picture.path)
        else:
            self.picture = self._meta.get_field('picture').get_default()
            self.save()
