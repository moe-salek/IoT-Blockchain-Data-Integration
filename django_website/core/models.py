import re

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


class Base(models.Model):
    id = models.BigAutoField(primary_key=True)
    model_created_at = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    model_modified_at = AutoDateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("User must have a username")
        pattern = re.compile("^(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$")
        if not pattern.match(username):
            raise ValueError("Given username is not valid")
        username = username.lower()
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, null=False, blank=False, unique=True,
                                validators=[MinLengthValidator(5)])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "username"


class Notification(Base):
    event_index = models.PositiveIntegerField()
    event_message = models.CharField(max_length=255)
    event_sensor_data = models.JSONField()

    def __str__(self):
        return f'Notification - {self.id}'


class MiddlewareFilter(Base):
    class Meta:
        verbose_name_plural = "Middleware Filters"

    name = models.CharField(max_length=255, default='Middleware Filters')
    interval_publish_to_broker = models.FloatField(default=3, verbose_name='Broker Publish Interval')
    interval_publish_to_blockchain = models.FloatField(default=5, verbose_name='Blockchain Publish Interval')
    high_temp_range = models.FloatField(default=35, verbose_name='High Temperature Range')
    low_temp_range = models.FloatField(default=10, verbose_name='Low Temperature Range')

    def __str__(self):
        return 'Middleware Filters'
