"""
Django settings for myus project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
import dj_database_url
from dotenv.main import load_dotenv

import django
from django.db import models
from django.db.models import Model

load_dotenv(override=True)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

host_url = os.getenv("HOST_URL")
ALLOWED_HOSTS = [host_url]

if os.getenv("CSRF_TRUSTED_EXTRA"):
    CSRF_TRUSTED_ORIGINS = ["https://" + host_url, os.getenv("CSRF_TRUSTED_EXTRA")]
    CSRF_TRUSTED_ORIGINS = [
        "https://" + host_url,
        "https://www." + host_url,
        os.getenv("CSRF_TRUSTED_EXTRA"),
    ]
else:
    CSRF_TRUSTED_ORIGINS = ["https://" + host_url]
    CSRF_TRUSTED_ORIGINS = ["https://" + host_url, "https://www." + host_url]

# Application definition
INSTALLED_APPS = [
    "myus.apps.myusConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "wsgi.application"

SECRET_KEY = os.getenv("SECRET_KEY")
POSTGRES_URL = os.getenv("DATABASE_URL")

DATABASES = {
    "default": dj_database_url.config(
        default=POSTGRES_URL, conn_max_age=0, ssl_require=True
    ),
}

AUTH_USER_MODEL = "myus.User"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# STATIC_ROOT = os.path.normpath(BASE_DIR)
# STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(os.path.normpath(BASE_DIR), "staticfiles")
STATIC_URL = os.path.join(os.path.normpath(BASE_DIR), "static/")

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "/"

# settings to silence Django errors
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_PRELOAD = False

# what errors to silence when running this
SILENCED_SYSTEM_CHECKS = ["security.W018", "security.W020", "models.W042"]
SILENCED_SYSTEM_CHECKS = []
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# https://docs.djangoproject.com/en/3.1/topics/logging/

# Loggers and handlers both have a log level; handlers ignore messages at lower
# levels. This is useful because a logger can have multiple handlers with
# different log levels.

# The levels are DEBUG < INFO < WARNING < ERROR < CRITICAL. DEBUG logs a *lot*,
# like exceptions every time a template variable is looked up and missing,
# which happens literally all the time, so that might be a bit too much.

# If you want to log to stdout (e.g. on Heroku), the handler looks as follows:
# {
#     'level': 'INFO',
#     'class': 'logging.StreamHandler',
#     'stream': sys.stdout,
#     'formatter': 'django',
# },

LOGGING = {
    "version": 1,  # the dictConfig format version
    "disable_existing_loggers": False,  # retain the default loggers
    "formatters": {
        "django": {
            "format": "%(asctime)s (PID %(process)d) [%(levelname)s] %(module)s\n%(message)s"
        },
    },
    "handlers": {
        "django": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "django",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["django"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
