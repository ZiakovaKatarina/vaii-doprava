from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrátor'),
        ('registered', 'Registrovaný používateľ'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='registered',
        verbose_name='Rola používateľa'
    )

    def __str__(self):
        return self.username