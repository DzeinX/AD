from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    number_phone = models.CharField(max_length=15, null=False, blank=False)
    email = models.CharField(max_length=50, null=False, blank=False)
    company_name = models.CharField(max_length=100, null=False, blank=False)
