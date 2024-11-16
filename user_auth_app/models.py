from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    BUSINESS = 'business'
    CUSTOMER = 'customer'
    PROFILE_TYPES = [
        (BUSINESS, 'business'),
        (CUSTOMER, 'customer'),
    ]

    username = models.CharField(max_length=150, unique=True, verbose_name="Benutzername")
    email = models.EmailField(unique=True, verbose_name="E-Mail-Adresse")
    password = models.CharField(max_length=128, verbose_name="Passwort")
    type = models.CharField(
        max_length=50,
        choices=PROFILE_TYPES,
        verbose_name="Profiltyp",
    )

    def __str__(self):
        return f"{self.username} ({self.get_type_display()})"