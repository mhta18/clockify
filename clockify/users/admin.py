from django.contrib import admin
from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    
    list_display = ("id","email", "first_name", "last_name", "created_at", "updated_at")

    readonly_fields = ("id","created_at", "updated_at")
