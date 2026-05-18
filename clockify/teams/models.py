from django.db import models
from django.utils.text import slugify
from django.conf import settings
import uuid
from django.core.exceptions import ValidationError

# Create your models here.

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    description = models.TextField(blank=True,max_length=300)
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="supervised_teams",null=True,blank=False)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="teams")


    # supervisor has to exist in the list of members for each team
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
