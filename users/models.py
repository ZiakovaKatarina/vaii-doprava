from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrátor'),
        ('registered', 'Registrovaný používateľ'),
    ]
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='registered',
        verbose_name='Rola'
    )
    phone = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name='Telefón'
    )
    
    class Meta:
        db_table = 'users_user'  # Explicitne nastavíme názov tabuľky
        verbose_name = 'Používateľ'
        verbose_name_plural = 'Používatelia'
    
    def is_admin(self):
        """Kontrola či používateľ je administrátor"""
        return self.role == 'admin'
    
    def is_registered_user(self):
        """Kontrola či používateľ je registrovaný (nie návštevník)"""
        return self.is_authenticated
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"