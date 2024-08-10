from django.db import models
from django.contrib.auth.models import AbstractUser

from core.mixins import TimestampMixin  


class User(AbstractUser, TimestampMixin):
    def __str__(self):
        return self.username
