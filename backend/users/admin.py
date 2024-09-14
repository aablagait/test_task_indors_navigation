"""Админ-панель пользователя."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


User = get_user_model()

UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('bio', 'role')}),
)


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     """Админ-панель пользователя."""
#
#     search_fields = ('email', 'username')
