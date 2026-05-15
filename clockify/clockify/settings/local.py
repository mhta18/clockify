from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'clockify',
        'HOST': 'localhost',
        'PORT': '1433',

        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
)

MEDIA_URL = "/media/" # access the uploaded file
MEDIA_ROOT = BASE_DIR / "media" # store the file