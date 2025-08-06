from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "username","telegram_id", "phone", "first_name", "last_name")
    search_fields = ("username", "phone", "first_name", "last_name")
    ordering = ("id",)
