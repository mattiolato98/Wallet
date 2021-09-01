from decimal import *
from math import log10, floor

from django.template.defaulttags import register

from asset_management.models import UserAsset
from transaction_management.models import Buy


@register.filter
def user_asset(user, asset):
    return UserAsset.objects.get(user=user, asset=asset)


@register.filter
def portfolio(userasset):
    return userasset.portfolio


@register.filter
def sort_by(objects, ordering):
    return objects.order_by(ordering)


@register.filter
def split(element, separator):
    return element.split(separator)


@register.filter
def select(obj, index):
    return obj[index] if index < len(obj) else obj[index - len(obj)]


@register.filter
def is_buy(obj):
    return True if isinstance(obj, Buy) else False


@register.filter
def round_float(number):
    if number > 1000:
        return round(number, 4)
    else:
        return round(number, 8)
