from django.contrib import admin

from transaction_management.models import Buy, Sell

admin.site.register(Buy)
admin.site.register(Sell)