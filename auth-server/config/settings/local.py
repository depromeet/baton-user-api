from .base import *

import environ


DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']

BASE_URL = 'http://127.0.0.1:8080/'  # kakao oauth function view에서 사용
USER_API_BASE_URL = 'http://host.docker.internal:8000/user/'
SEARCH_API_BASE_URL = 'https://baton.yonghochoi.com/search/'


env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env.local')


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
