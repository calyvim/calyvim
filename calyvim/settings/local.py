import os
from calyvim.settings.base import *

ALLOWED_HOSTS = ["*"]
DEBUG = True

RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY", "0x4AAAAAAAVK************")
RECAPTCH_SECRET_KEY = os.environ.get("RECAPTCH_SECRET_KEY", "0x4AAAAAA*****************")
RECAPTCHA_ENABLED = False