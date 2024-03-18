import os
import dj_database_url

from calyvim.settings.base import *

ALLOWED_HOSTS = ["calyvim.com", "calyvim-8179bcb6855b.herokuapp.com"]
DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get("DATABASE_URL"))
}