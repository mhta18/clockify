from django.db import models
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class Contract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contracts")
    role_title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role_title} - {self.user.email}"



class FreelancerContract(Contract):
    hourly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    daily_hours_required = models.PositiveIntegerField()
    document_file = models.FileField(
        upload_to="contracts/freelancers/", null=True, blank=True
    )


class EmployerContract(Contract):
    class EmploymentType(models.TextChoices):
        PART_TIME = "PART_TIME", "Part-time"
        FULL_TIME = "FULL_TIME", "Full-time"

    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices)
