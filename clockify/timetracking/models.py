from django.db import models
from users.models import User
from projects.models import Project
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
from decimal import Decimal
from contracts.models import FreelancerContract, EmployerContract
# Create your models here.


class TimeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="time_logs")
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="time_logs"
    )
    description = models.CharField(max_length=500, blank=False)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    payment = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    class Meta:
        ordering = ["-start_time"]

    @property
    def duration(self):
        if not self.end_time:
            return timedelta(0)
        return self.end_time - self.start_time

    def clean(self):
        if self.end_time and self.end_time < self.start_time:
            raise ValidationError(
                {"end_time": "End time cannot be earlier than start time."}
            )

        # check if user does not have any contract or belongs to any team
        if not hasattr(self.user, "teams") or not self.user.teams.exists():
            raise ValidationError("You must belong to a team to track time.")
        if not hasattr(self.user, "contract"):
            raise ValidationError("You must have an active contract to track time.")

    def save(self, *file, **kwargs):

        if self.end_time and self.duration.total_seconds() > 0:
            duration_in_hours = Decimal(self.duration.total_seconds()) / Decimal(
                "3600.00"
            )
            if hasattr(self.user, 'contract'):
                base_contract = self.user.contract

                

                if hasattr(base_contract, 'freelancercontract'):
                    freelancer_contract = FreelancerContract.objects.filter(user=self.user).first()

                    hourly_payment = Decimal(str(freelancer_contract.hourly_payment))

                    duration_in_hours = Decimal(self.duration.total_seconds())/Decimal("3600.00")
                    self.payment = round(duration_in_hours * hourly_payment, 2)

                elif hasattr(base_contract, 'employercontract'):
                    employer_contract = EmployerContract.objects.filter(user = self.user).first()
                    worked_days_in_month = Decimal("22.00")
                    mountly_pay= Decimal(employer_contract.monthly_payment)
                    daily_hours= Decimal(employer_contract.employment_type)

                    implied_hourly_rate = mountly_pay / (worked_days_in_month * daily_hours)

                    self.payment = round(duration_in_hours * implied_hourly_rate,2)
                else:
                    self.payment = Decimal("0.00")
            else:
                self.payment = Decimal("0.00")
        else:
            self.payment = Decimal("0.00")
        self.full_clean()
        super().save(*file, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} - {self.project.name} - {self.duration}"
