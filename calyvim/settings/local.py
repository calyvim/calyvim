import os
from dotenv import load_dotenv
from calyvim.settings.base import *

load_dotenv()  # take environment variables from .env.

ALLOWED_HOSTS = ["*"]
DEBUG = True
SITE_URL = os.environ.get("SITE_URL", "http://127.0.0.1:8000")

RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY", "0x4AAAAAAAVK************")
RECAPTCH_SECRET_KEY = os.environ.get("RECAPTCH_SECRET_KEY", "0x4AAAAAA*****************")
RECAPTCHA_ENABLED = False

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "media" / "emails"  # change this to a proper location

# CELERY
CELERY_BROKER_URL = os.environ.get("REDISCLOUD_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("REDISCLOUD_URL", "redis://localhost:6379/0")
CELERY_TIMEZONE = "UTC"