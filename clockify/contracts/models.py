from django.db import models
from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Contract(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="contract")
    role_title = models.CharField(max_length=255)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
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
    class EmploymentHours(models.IntegerChoices):
        FOUR_HOURS = 4, "Part-time (4 Hours)"
        FIVE_HOURS = 5, "Part-time (5 Hours)"
        SIX_HOURS = 6, "Part-time (6 Hours)"
        SEVEN_HOURS = 7, "Part-time (7 Hours)"
        EIGHT_HOURS = 8, "Full-time (8 Hours)"

    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    employment_type = models.IntegerField(
        choices=EmploymentHours.choices,
        default=EmploymentHours.EIGHT_HOURS,
        validators=[MinValueValidator(4), MaxValueValidator(8)],
        help_text="Designated daily contractual obligation commitment hours.",
    )
