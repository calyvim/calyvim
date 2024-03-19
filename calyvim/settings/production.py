import os
import dj_database_url
import sentry_sdk

from calyvim.settings.base import *

ALLOWED_HOSTS = ["calyvim.com", "calyvim-8179bcb6855b.herokuapp.com"]
DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    enable_tracing=True,
)

DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))}

RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")
RECAPTCHA_ENABLED = True
