from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from offers_app.models import Offer, OfferDetail


@receiver([post_save, post_delete], sender=OfferDetail)
def update_offer_min_values(sender, instance, **kwargs):
    """
    Signal to update the offer's min_price and min_delivery_time when an
    OfferDetail is created, updated, or deleted.
    """
    offer = instance.offer
    offer_details = offer.details.all()

    if offer_details.exists():
        offer.min_price = min(offer_details, key=lambda x: x.price).price
        offer.min_delivery_time = min(offer_details, key=lambda x: x.delivery_time_in_days).delivery_time_in_days
    else:
        offer.min_price = None
        offer.min_delivery_time = None

    offer.save()
