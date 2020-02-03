from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, \
    PermissionsMixin, BaseUserManager
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


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
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%s' % self.name


@receiver(pre_save, sender=User)
def set_default_name_from_email(sender, instance, **kwargs):
    if not instance.name:
        email = str(instance.email)
        instance.name = email


class Blog(models.Model):
    """
    blog model.
    user 1-m blog
    """
    title = models.CharField(max_length=255, unique=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # name would be 'author_id' in database
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='blogs', on_delete=models.CASCADE)

    class Meta:
        ordering = ['updated', 'created']

    def __str__(self):
        return self.title

    def __unicode__(self):
        return '%s' % self.title
