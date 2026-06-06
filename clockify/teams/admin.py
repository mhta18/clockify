from django.contrib import admin

# Register your models here.
from .models import Team,Task

admin.site.register(Team)
admin.site.register(Task)
