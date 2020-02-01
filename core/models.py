from django.contrib.auth.models import AbstractBaseUser, \
    PermissionsMixin, BaseUserManager

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings


class UserManager(BaseUserManager):
    """
    Helps Django work with custom user model.
    Must define 'create_user', 'create_superuser'.
    Remember to add AUTH_USER_MODEL to settings.py
    """

    def create_user(self, email, password=None, **other_fields):
        """Create a new user."""
        if not email:
            raise ValueError("User must have an email.")

        user = self.model(email=self.normalize_email(email), **other_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """create to substitute default django user"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


@receiver(pre_save, sender=User)
def set_default_name_from_email(sender, instance, **kwargs):
    if not instance.name:
        email = str(instance.email)
        instance.name = email.split('.')[0]
