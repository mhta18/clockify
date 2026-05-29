import uuid
import os
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete
from users.models import User
from django.core.exceptions import ValidationError

# Create your models here.


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, max_length=300)
    logo = models.ImageField(upload_to="team_logos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="supervised_teams",
        null=True,
        blank=False,
    )
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="teams")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Task(models.Model):

    class Priority(models.TextChoices):
        HIGH = "HIGH", "High"
        MEDIUM = "MEDIUM", "Medium"
        LOW = "LOW", "Low"

    class Status(models.TextChoices):
        TODO = "TODO", "To Do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        REVIEW = "REVIEW", "Under Review"
        DONE = "DONE", "Done"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="tasks")

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_tasks"
    )
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assigned_tasks"
    )

    deadline = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
        help_text="The current operational lifecycle state of the task.",
    )
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()

        if self.team and self.created_by and self.team.supervisor != self.created_by:
            raise ValidationError(
                {
                    "created_by": f"{self.created_by.email} is not designated as the supervisor for the team '{self.team.name}'."
                }
            )

        if (
            self.team
            and self.assigned_to
            and self.assigned_to not in self.team.members.all()
        ):
            raise ValidationError(
                {
                    "assigned_to": f"{self.assigned_to.email} is not a member of the team '{self.team.name}'."
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


@receiver(post_delete, sender=Team)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)


@receiver(models.signals.pre_save, sender=Team)
def auto_delete_file_on_change(instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_logo = Team.objects.get(pk=instance.pk).logo
    except Team.DoesNotExist:
        return False

    new_logo = instance.logo

    if old_logo and old_logo != new_logo:
        if os.path.isfile(old_logo.path):
            os.remove(old_logo.path)
