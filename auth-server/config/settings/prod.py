from .base import *

import environ


DEBUG = False
ALLOWED_HOSTS = ['*']  # TODO 수정

BASE_URL = 'https://baton.yonghochoi.com/'  # kakao oauth function view에서 사용
USER_API_BASE_URL = 'https://baton.yonghochoi.com/user/'  # TODO kubernetes service domain name으로 대체
SEARCH_API_BASE_URL = 'https://baton.yonghochoi.com/search/'
# USER_API_BASE_URL = 'http://baton-user-api.baton.svc.cluster.local:8000/user/'
# SEARCH_API_BASE_URL = 'http://baton-search-api.baton.svc.cluster.local:8080/search/'


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

REST_FRAMEWORK.update({
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
})

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
