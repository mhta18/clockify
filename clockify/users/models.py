from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
import os

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)

        return self.create_user(email, password, **extra_fields)


class User(
    AbstractBaseUser,
    PermissionsMixin,
):

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    email = models.EmailField(unique=True)

    first_name = models.CharField(
        max_length=255,
        blank=True,
    )

    last_name = models.CharField(
        max_length=255,
        blank=True,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=False,
        null=False,
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
    )

    age = models.PositiveIntegerField(
        null=True,  
        blank=True,
    )

    country = models.CharField(
        max_length=255,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [gender]
    

    objects = UserManager()

    def __str__(self):

        return self.email


# A Signal to delete the avatar file when the user is deleted
@receiver(post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)

# A Signal to delete the old avatar file when the user updates the avatar
@receiver(models.signals.pre_save, sender=User)
def auto_delete_file_on_change(instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_avatar = User.objects.get(pk=instance.pk).avatar
    except User.DoesNotExist:
        return False

    new_avatar = instance.avatar

    if not old_avatar == new_avatar:
        if os.path.isfile(old_avatar.path):
            os.remove(old_avatar.path)
