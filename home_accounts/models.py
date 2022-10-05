from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    is_vendor = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'gender', 'is_vendor']
