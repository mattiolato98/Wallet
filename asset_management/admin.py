from django.contrib import admin

from asset_management.models import UserAsset, Asset, Url, Tag, Fiat, UserPortfolio

admin.site.register(UserAsset)
admin.site.register(Asset)
admin.site.register(Url)
admin.site.register(Tag)
admin.site.register(Fiat)
admin.site.register(UserPortfolio)
