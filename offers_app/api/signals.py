from django.db.models.signals import post_save
from django.dispatch import receiver
from offers_app.models import OfferDetail, Offer

@receiver(post_save, sender=OfferDetail)
def update_offer_min_values(sender, instance, created, **kwargs):
    """Signal that updates the offer's min_price and min_delivery_time 
       when an OfferDetail is created or updated.
    """
    
    offer = instance.offer
    offer_details = offer.details.all()
    
    min_price = min(offer_details, key=lambda x: x.price).price
    min_delivery_time = min(offer_details, key=lambda x: x.delivery_time_in_days).delivery_time_in_days

    offer.min_price = min_price
    offer.min_delivery_time = min_delivery_time
    
    offer.save()