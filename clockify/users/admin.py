from django.contrib import admin
from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # This automatically lists the timestamps as columns in your admin table dashboard!
    list_display = ("email", "first_name", "last_name", "created_at", "updated_at")

    # This forces Django to show the uneditable timestamps inside the user edit form!
    readonly_fields = ("created_at", "updated_at")
