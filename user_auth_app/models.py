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

    def __str__(self):
        return f"{self.username} ({self.get_type_display()})"