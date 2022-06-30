from .base import *
import environ


DEBUG = False
ALLOWED_HOSTS = ['*']  # TODO 수정
# ALLOWED_HOSTS = ['baton-user-api.baton.svc.cluster.local']

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env.prod')


# Secrets
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


# Parser and Renderer
REST_FRAMEWORK.update({
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
})

SWAGGER_SETTINGS['SUPPORTED_SUBMIT_METHODS'] = []

# HTTP header
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# AWS S3
AWS_S3_ACCESS_KEY_ID = env('AWS_S3_ACCESS_KEY_ID')
AWS_S3_SECRET_ACCESS_KEY = env('AWS_S3_SECRET_ACCESS_KEY')
AWS_REGION = 'ap-northeast-2'

AWS_STORAGE_BUCKET_NAME = 'depromeet11th'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL = 'public-read-write'
AWS_LOCATION = '6team'
STATIC_LOCATION = f'{AWS_LOCATION}/'.lstrip('/') + 'static/user-api'
MEDIA_LOCATION = f'{AWS_LOCATION}/'.lstrip('/') + 'media/user-api'

# Storage Backend
DEFAULT_FILE_STORAGE = 'config.storages.MediaS3Boto3Storage'
STATICFILES_STORAGE = 'config.storages.StaticS3Boto3Storage'

# Static files (CSS, JavaScript, Images)
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
STATICFILES_DIRS = []  # additional locations the staticfiles app will traverse.
