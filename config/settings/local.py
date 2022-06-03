from .base import *

import os
import json


DEBUG = True
ALLOWED_HOSTS = []
BASE_URL = 'http://127.0.0.1:8000/'

# Environment variable setting
secret_file = os.path.join(BASE_DIR, 'secrets.json')  # secrets.json 파일 위치를 명시

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = f'Set the {setting} environment variable'
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret("SECRET_KEY")
DATABASES = get_secret('DATABASES_LOCAL')
KAKAO_REST_API_KEY = get_secret('KAKAO_REST_API_KEY')
