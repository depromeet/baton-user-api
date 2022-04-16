# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    user = models.OneToOneField('accounts.SocialUser', primary_key=True, on_delete=models.CASCADE, db_column='id')
    nickname = models.CharField(max_length=255)
    gender = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'


class Bookmark(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, related_name='bookmarks')
    ticket = models.ForeignKey('Ticket', models.DO_NOTHING, related_name='bookmarks')

    class Meta:
        managed = False
        db_table = 'Bookmark'


class Tag(models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()
    users = models.ManyToManyField('User', through='UserTag', related_name='tags')

    class Meta:
        managed = False
        db_table = 'Tag'


class Ticket(models.Model):
    seller = models.ForeignKey('User', models.DO_NOTHING, related_name='sell_tickets')
    buyer = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True, related_name='buy_tickets')
    bookmark_users = models.ManyToManyField('User', through='Bookmark', related_name='bookmark_tickets')
    tags = models.ManyToManyField('Tag', through='TicketTag', related_name='tickets')
    location = models.CharField(max_length=255)
    price = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Ticket'


class TicketTag(models.Model):
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING)
    tag = models.ForeignKey(Tag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'TicketTag'


class UserTag(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    tag = models.ForeignKey(Tag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'UserTag'
