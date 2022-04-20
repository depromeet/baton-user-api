from django.apps import apps
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class SocialUserManager(BaseUserManager):
    def _create_user(self, social_id, provider, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not (social_id or provider):
            raise ValueError('The given id and provider must be set')
        user = self.model(social_id, provider, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, social_id, provider, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(social_id, provider, password, **extra_fields)

    def create_superuser(self, social_id, provider, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(social_id, provider, password, **extra_fields)


class SocialUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    social_id = models.CharField(_('uid'), max_length=255)
    provider = models.CharField(_('provider'), max_length=30)

    objects = SocialUserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['provider', 'social_id']

    class Meta:
        verbose_name = _('social user')
        verbose_name_plural = _('social users')

    # def clean(self):
    #     super().clean()
    #     self.email = self.__class__.objects.normalize_email(self.email)

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        """All superusers are staff"""
        return self.is_superuser
