from .base import *

print("setting: DEV")

DEBUG = True

ALLOWED_HOSTS = ["*"]

# LOGGING["loggers"]['']["level"] = "DEBUG"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

