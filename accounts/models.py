
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('member', 'Member'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='member'
    )

    contact_number = models.CharField(
        max_length=15,
        blank=True
    )

    def __str__(self):
        return self.username
