from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

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
    

class Review(models.Model):
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_reviews",
        on_delete=models.CASCADE,
        limit_choices_to={'type': 'business'},
        verbose_name="Geschäftsbenutzer"
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="given_reviews",
        on_delete=models.CASCADE,
        limit_choices_to={'type': 'customer'},
        verbose_name="Kunden-Bewerter"
    )
    rating = models.PositiveSmallIntegerField(validators=[
            MaxValueValidator(5)
        ])  # z. B. 1-5
    description = models.TextField(verbose_name="Beschreibung", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business_user', 'reviewer')  # Ein Reviewer kann nur eine Bewertung pro Business User abgeben
        ordering = ['-updated_at']

    def __str__(self):
        return f"Review von {self.reviewer} für {self.business_user} - {self.rating} Sterne"    