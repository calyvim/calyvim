import os
import dj_database_url
import sentry_sdk
import re

from calyvim.settings.base import *

# Vite generates files with 8 hash digits
# http://whitenoise.evans.io/en/stable/django.html#WHITENOISE_IMMUTABLE_FILE_TEST

def immutable_file_test(path, url):
    # Match filename with 12 hex digits before the extension
    # e.g. app.db8f2edc0c8a.js
    return re.match(r"^.+[\.\-][0-9a-f]{8,12}\..+$", url)

DEBUG = False

ALLOWED_HOSTS = ["calyvim.com", "calyvim-81593360e924.herokuapp.com"]
CSRF_TRUSTED_ORIGINS = ["https://calyvim.com", "https://calyvim-81593360e924.herokuapp.com"]
CORS_ALLOWED_ORIGINS = ["calyvim.com", "calyvim-81593360e924.herokuapp.com"]
CORS_URLS_REGEX = r"^/api/.*$"

SECRET_KEY = os.environ.get("SECRET_KEY")
SITE_URL = os.environ.get("SITE_URL", "https://calyvim.com")

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    enable_tracing=True,
)

DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))}

RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")
RECAPTCHA_ENABLED = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_USE_TLS = True
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# CELERY
CELERY_BROKER_URL = os.environ.get("REDISCLOUD_URL")
CELERY_RESULT_BACKEND = os.environ.get("REDISCLOUD_URL")
CELERY_TIMEZONE = "UTC"

GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")

# Django Vite Setup
DJANGO_VITE_DEV_MODE = False
WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test
DJANGO_VITE_STATIC_URL_PREFIX = "dist"
