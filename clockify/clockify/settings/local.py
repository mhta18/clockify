from .base import *
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = True
TEMPLATES[0]["DIRS"] = [Path(__file__).resolve().parent.parent / "templates"]
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

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
