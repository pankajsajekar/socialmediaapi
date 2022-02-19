from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)

        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    first_name = None
    last_name = None
    user_full_name = models.CharField(max_length=100, null=True)
    objects = UserManager()

    class Meta:
        verbose_name_plural = '1. Users'

    def _str_(self):
        return self.username

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, models.SET_NULL, related_name="request_sender", blank=True, null=True)
    receiver = models.ForeignKey(User, models.SET_NULL, related_name="request_receiver", blank=True, null=True)
    status = models.CharField(max_length=100,
                                             choices=(('pending', 'pending'), ('accept', 'accept'),
                                                      ('reject','reject')))

    def __str__(self):
        template = 'request came from {0.sender} to {0.receiver} status is {0.status} '
        return  template.format(self)