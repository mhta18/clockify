from django.contrib import admin
from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    
    list_display = ("email", "first_name", "last_name", "created_at", "updated_at")

    readonly_fields = ("created_at", "updated_at")
