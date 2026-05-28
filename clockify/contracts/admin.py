from django.contrib import admin
from .models import FreelancerContract, EmployerContract
# Register your models here.
admin.site.register(EmployerContract)
admin.site.register(FreelancerContract)