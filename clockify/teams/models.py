import uuid
import os
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete

# Create your models here.

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100,unique=True)
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

    if old_logo and old_logo != new_logo :
        if os.path.isfile(old_logo.path):
            os.remove(old_logo.path)
 