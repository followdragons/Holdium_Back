from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from _auth.models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('telegram_id', 'username_tg', 'first_name', 'last_name', 'evm_address', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('telegram_id', 'username_tg', 'first_name', 'last_name', 'evm_address')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('telegram_id', 'password')}),
        ('Personal info', {'fields': ('username_tg', 'first_name', 'last_name', 'evm_address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )