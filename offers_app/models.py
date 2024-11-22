from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Offer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='offers', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    min_delivery_time = models.PositiveIntegerField(blank=True, null=True)

    def clean(self):
        # Validierung sicherstellen, dass nur Business-Benutzer Angebote erstellen können
        if self.user.user_type != 'business':
            raise ValidationError('Nur Business-Nutzer können Angebote erstellen.')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class OfferDetail(models.Model):
    offer = models.ForeignKey(Offer, related_name='details', on_delete=models.CASCADE)
    offer_type = models.CharField(max_length=20, choices=[
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ])
    
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()  # -1 für unendlich viele Revisionen
    delivery_time_in_days = models.PositiveIntegerField()  # Lieferzeit in Tagen
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()  # Features als JSON (Liste der Features)

    def __str__(self):
        return f"{self.offer_type.capitalize()} Detail: {self.title}"

    class Meta:
        ordering = ['offer_type']
