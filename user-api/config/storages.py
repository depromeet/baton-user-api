from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticS3Boto3Storage(S3Boto3Storage):
    location = getattr(settings, 'STATIC_LOCATION')


class MediaS3Boto3Storage(S3Boto3Storage):
    location = getattr(settings, 'MEDIA_LOCATION')
    file_overwrite = False  # TODO 필요?
