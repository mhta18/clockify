import uuid
from django.db import models
from django.utils.text import slugify
from teams.models import Team
# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100,unique=True)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True,primary_key=True)
    slug = models.SlugField(max_length=255,unique=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True )
    end_date = models.DateTimeField(null=True,blank=True)

    teams = models.ManyToManyField(Team,related_name="projects",blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    