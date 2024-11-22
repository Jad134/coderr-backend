from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class  CustomUser(AbstractUser):
    BUSINESS = 'business'
    CUSTOMER = 'customer'
    PROFILE_TYPES = [
        (BUSINESS, 'business'),
        (CUSTOMER, 'customer'),
    ]

    type = models.CharField(
        max_length=50,
        choices=PROFILE_TYPES,
        verbose_name="Profiltyp",
    )
    first_name = models.CharField(max_length=150, blank=True, verbose_name="Vorname")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Nachname")
    file = models.FileField(upload_to="profile_pictures/", blank=True, null=True, verbose_name="Profilbild")
    location = models.CharField(max_length=255, blank=True, verbose_name="Standort")
    tel = models.CharField(max_length=20, blank=True, verbose_name="Telefonnummer")
    description = models.TextField(blank=True, verbose_name="Beschreibung")
    working_hours = models.CharField(max_length=255, blank=True, verbose_name="Arbeitszeiten")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")

    def __str__(self):
        return f"{self.username} ({self.get_type_display()})"