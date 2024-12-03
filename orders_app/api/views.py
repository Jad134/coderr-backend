from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from offers_app.models import OfferDetail
from orders_app.api.serializers import OrderSerializer
from orders_app.models import Order
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination


class OrderViewSet(viewsets.ViewSet):

    def get_queryset(self):
        return Order.objects.all()

    def list(self, request):
        """
        Get order list with queryset for filter methods in Frontend Code e.g only show own offers with creator_id
        """
        queryset = self.get_queryset()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)
    

    def create(self, request):
        """
        POST /orders/
        Create an new Order based on OfferDetail.
        """
        # Authentifizierung sicherstellen
        customer_user = request.user
        if customer_user.type != 'customer':
            return Response(
                {'detail': 'Nur Kunden können Bestellungen erstellen.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # `offer_detail_id` aus dem Anfrage-Body validieren
        offer_detail_id = request.data.get('offer_detail_id')
        if not offer_detail_id:
            return Response(
                {'detail': 'Das Feld "offer_detail_id" ist erforderlich.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # OfferDetail-Objekt abrufen und prüfen
        offer_detail = get_object_or_404(OfferDetail, id=offer_detail_id)

        # Anbieter des Angebots (Business-User) abrufen
        business_user = offer_detail.offer.user

        # Bestellung erstellen
        order_data = {
            "customer_user": customer_user.id,
            "business_user": business_user.id,
            "title": offer_detail.title,
            "revisions": offer_detail.revisions,
            "delivery_time_in_days": offer_detail.delivery_time_in_days,
            "price": offer_detail.price,
            "features": offer_detail.features,
            "offer_type": offer_detail.offer_type,
            "status": "in_progress",
        }
        serializer = OrderSerializer(data=order_data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    