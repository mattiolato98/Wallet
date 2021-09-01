from django.contrib import admin
from user_management.models import PlatformUser, Profile

admin.site.register(PlatformUser)
admin.site.register(Profile)
