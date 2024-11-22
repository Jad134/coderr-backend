from django.db import models
from django.conf import settings

class Order(models.Model):
    # Die Beziehung zu den Benutzer-Modellen
    customer_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customer_orders', on_delete=models.CASCADE)
    business_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='business_orders', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)  # JSONField speichert Listen und Dictionaries als JSON

    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('exclusive', 'Exclusive'),
    ]
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES, default='basic')

    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Neueste Bestellung zuerst.
