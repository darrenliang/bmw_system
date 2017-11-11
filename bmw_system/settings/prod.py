from .base import *

print("setting: PROD")

DEBUG = False

# LOGGING["loggers"]['']["level"] = "DEBUG"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

