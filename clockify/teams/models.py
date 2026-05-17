from django.db import models
from django.utils.text import slugify
from django.conf import settings
import uuid

# Create your models here.

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    description = models.TextField(blank=True,max_length=300)
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)
    number_of_members = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="teams")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name