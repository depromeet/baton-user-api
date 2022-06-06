from .base import *

import environ


DEBUG = False
ALLOWED_HOSTS = ['*']  # TODO 수정

BASE_URL = 'https://baton.yonghochoi.com/'


env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env.prod')


SECRET_KEY = env("SECRET_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DATABASES_NAME"),
        "USER": env("DATABASES_USER"),
        "PASSWORD": env("DATABASES_PASSWORD"),
        "HOST": env("DATABASES_HOST"),
        "PORT": env("DATABASES_PORT"),
    }
}

KAKAO_REST_API_KEY = env('KAKAO_REST_API_KEY')
