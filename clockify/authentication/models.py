from django.db import models
from datetime import timedelta
from django.utils import timezone
from clockify.settings.base import OTP_EXPIRE_MINUTES


class LoginOTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(OTP_EXPIRE_MINUTES)

    def __str__(self):
        return self.email
