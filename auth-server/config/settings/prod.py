from .base import *

import os
from dotenv import load_dotenv


DEBUG = False
ALLOWED_HOSTS = ['*']  # TODO 수정

BASE_URL = 'https://baton.yonghochoi.com/'

load_dotenv()


def get_secret(setting):
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = f'Set the {setting} environment variable'
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret("SECRET_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": get_secret("DATABASES_NAME"),
        "USER": get_secret("DATABASES_USER"),
        "PASSWORD": get_secret("DATABASES_PASSWORD"),
        "HOST": get_secret("DATABASES_HOST"),
        "PORT": get_secret("DATABASES_PORT"),
    }
}

KAKAO_REST_API_KEY = get_secret('KAKAO_REST_API_KEY')
