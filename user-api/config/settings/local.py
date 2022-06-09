from .base import *

import environ


DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'host.docker.internal']
BASE_URL = 'http://127.0.0.1:8000/'

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env.local')


SECRET_KEY = env("SECRET_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.mysql",
        "NAME": env("DATABASES_NAME"),
        "USER": env("DATABASES_USER"),
        "PASSWORD": env("DATABASES_PASSWORD"),
        "HOST": env("DATABASES_HOST"),
        "PORT": env("DATABASES_PORT"),
    }
}
