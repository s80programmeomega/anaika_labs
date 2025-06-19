from django.contrib import admin
from .models import CustomUser, UserType


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "username", "user_type", "is_active", "is_staff")
    list_display_links = ("id", "email", "username")
    search_fields = ("email", "username")
    list_filter = ("user_type", "is_active", "is_staff")
