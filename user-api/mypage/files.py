from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile

from config.storages import StaticS3Boto3Storage, MediaS3Boto3Storage


class DynamicStorageImageFieldFile(ImageFieldFile):
    def __init__(self, instance, field, name):
        super().__init__(instance, field, name)
        if instance.is_custom_image:
            self.storage = MediaS3Boto3Storage()
        else:
            self.storage = StaticS3Boto3Storage()


class DynamicStorageImageField(ImageField):
    attr_class = DynamicStorageImageFieldFile
