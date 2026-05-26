from django.db import models
from users.models import User
from projects.models import Project
from django.utils import timezone
from django.core.exceptions import ValidationError

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

    class Meta:
        ordering = ["-start_time"]

    @property
    def duration(self):
        if not self.end_time:
            return timezone.now() - self.start_time
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
