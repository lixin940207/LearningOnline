from django.contrib import admin

from apps.users.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    pass

# admin.site.register(UserProfile, UserProfileAdmin)