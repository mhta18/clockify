import uuid
from django.db import models
from django.utils.text import slugify
from teams.models import Team
from django.core.validators import RegexValidator
# Create your models here.

hex_color_validator = RegexValidator(
    regex=r"^#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6})$",
    message="Color must be a valid hex code starting with '#' (e.g., #FFF or #FF5733).",
)
class Project(models.Model):
    name = models.CharField(max_length=100,unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    slug = models.SlugField(max_length=255,unique=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True )
    end_date = models.DateTimeField(null=True,blank=True)
    color = models.CharField(max_length=7,default="#D1D5DB")
    teams = models.ManyToManyField(Team,related_name="projects",blank=True)

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter +=1

            self.slug = slug
        super().save(*args,**kwargs)
