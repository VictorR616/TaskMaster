from taskmaster.settings.base import *

SECRET_KEY = "dsoihwe23SDHWO2nfrer=)"

DEBUG = True


ALLOWED_HOSTS = []


# Configuración en desarrollo
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

