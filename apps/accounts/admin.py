from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display   = ['email', 'username', 'first_name', 'last_name', 'balance', 'is_email_verified', 'is_active', 'is_staff']
    readonly_fields = ['balance', 'is_email_verified']
    list_filter    = ['is_email_verified', 'is_active', 'is_staff']
    search_fields  = ['email', 'username', 'first_name', 'last_name']
    ordering       = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('Roomsy Info', {
            'fields': ('balance', 'is_email_verified', 'phone_number')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Roomsy Info', {
            'fields': ('email', 'first_name', 'last_name', 'balance', 'is_email_verified')
        }),
    )
