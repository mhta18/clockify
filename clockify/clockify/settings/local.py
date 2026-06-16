from .base import *

DEBUG = True
SECRET_KEY = "django-insecure-local-development-key-leave-this-here"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "clockify",
        "USER": "postgres",
        "PASSWORD": "m.mira1183",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = "mahta.m.1183@gmail.com"
EMAIL_HOST_PASSWORD = "dmrgavyaoggwwyou"

DEFAULT_FROM_EMAIL = "mahta.m.1183@gmail.com"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
