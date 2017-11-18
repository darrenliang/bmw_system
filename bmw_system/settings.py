"""
Django settings for bmw project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from logging.handlers import DEFAULT_TCP_LOGGING_PORT

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!p_&x!rv9(u*aaeubn^5vwjri=82d72*4$skea7&v2knwapf2_'

DEBUG = True
ALLOWED_HOSTS = ["*"]

# LOGGING["loggers"]['']["level"] = "DEBUG"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',

    'channels',
    "solo",
    'bmw.apps.BmwConfig',
    'rest_framework.authtoken',
    'logentry_admin',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    # 'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bmw_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bmw_system.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Hong_Kong'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
]


# # Logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'simple': {
#             'format': '%(asctime)s %(levelname)s %(message)s',
#             'datefmt': '%H:%M:%S',
#         },
#         'verbose': {
#             'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#             'datefmt': '%m-%d %H:%M:%S',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'WARNING',
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple',
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'share.socket_logging.SocketHandler',
#             'host': 'localhost',
#             'port': DEFAULT_TCP_LOGGING_PORT,
#             'formatter': 'verbose',
#             # 'encoding': "utf-8",
#         },
#         # 'file': {
#         #     'level': 'DEBUG',
#         #     'class': 'logging.FileHandler',
#         #     'filename': os.path.join(BASE_DIR, 'logs', 'django.%s.log' % strftime("%Y%m%d")),
#         #     'formatter': 'verbose',
#         #     'encoding': "utf-8",
#         # },
#         # 'err_file': {
#         #     'level': 'ERROR',
#         #     'class': 'logging.FileHandler',
#         #     'filename': os.path.join(BASE_DIR, 'logs', 'django.error.%s.log' % strftime("%Y%m%d")),
#         #     'formatter': 'verbose',
#         #     'encoding': "utf-8",
#         # },
#     },
#     'loggers': {
#         '': {
#             'level': 'DEBUG',
#             'handlers': ['console', 'file', ],
#             'propagate': False,
#         },
#         'django': {
#             'propagate': True,
#             'level': 'INFO'
#         },
#         'fishing': {
#             'propagate': True,
#             'level': 'DEBUG',
#         },
#         'daphne': {
#             'propagate': True,
#             'level': 'INFO',
#         },
#         'requests': {
#             'propagate': True,
#             'level': 'INFO',
#         },
#         'django.channels': {
#             'propagate': True,
#             'level': 'WARNING',
#         },
#     },
# }

REDIS_CACHE = "redis://localhost:6379/3"
REDIS_QUEUE = "redis://localhost:6379/4"

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': [REDIS_CACHE],
        'OPTIONS': {
            'PASSWORD': '',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            },
            'MAX_CONNECTIONS': 1000,
            'PICKLE_VERSION': -1,
        },
    },
}

# Channel settings
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "asgi_redis.RedisChannelLayer",
#         'ROUTING': 'fishing.routing.channel_routing',
#         "CONFIG": {
#             "hosts": [REDIS_QUEUE],
#             "expiry": 60,
#             "capacity": 100,
#         },
#     },
# }

