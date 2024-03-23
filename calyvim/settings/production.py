import os
import dj_database_url
import sentry_sdk

from calyvim.settings.base import *

ALLOWED_HOSTS = ["calyvim.com", "calyvim-8179bcb6855b.herokuapp.com"]
CSRF_TRUSTED_ORIGINS = ["https://calyvim.com", "https://calyvim-8179bcb6855b.herokuapp.com"]
DEBUG = False
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