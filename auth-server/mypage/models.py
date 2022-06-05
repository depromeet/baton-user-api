# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.conf import settings

TEST = False


class User(models.Model):
    id = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE,
                              db_column='id', related_name='app_user', help_text='User ID(integer)')
    # id = models.IntegerField(primary_key=True, )
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    created_on = models.DateField(auto_now_add=True)
    account = models.OneToOneField('Account', blank=True, null=True, on_delete=models.CASCADE)  # TODO has_account 추가?
    # point = models.PointField()
    address = models.CharField(max_length=255)
    detailed_address = models.CharField(max_length=255, blank=True)
    check_terms_of_service = models.BooleanField()
    check_privacy_policy = models.BooleanField()  # TODO model_schema.sql

    class Meta:
        managed = TEST
        db_table = 'User'


class Account(models.Model):
    holder = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)
    number = models.CharField(max_length=255)

    class Meta:
        managed = TEST
        db_table = 'Account'
