from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from offers_app.models import OfferDetail
from orders_app.api.serializers import OrderSerializer
from orders_app.models import Order
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from user_auth_app.models import CustomUser


class OrderViewSet(viewsets.ViewSet):

    def get_queryset(self):
        return Order.objects.all()

    def list(self, request):
       """
       GET /orders/
       List orders associated with the logged-in user.
       """
       user = request.user
   
       if user.type == "customer":
           queryset = self.get_queryset().filter(customer_user=user)
       elif user.type == "business":
           queryset = self.get_queryset().filter(business_user=user)
       else:
           return Response(
               {"detail": "Ungültiger Benutzertyp."},
               status=status.HTTP_403_FORBIDDEN,
           )

       serializer = OrderSerializer(queryset, many=True)
       return Response(serializer.data)
    

    def create(self, request):
       """
       POST /orders/
       Create a new order based on OfferDetail.
       """
       if not self.is_customer(request.user):
           return self.forbidden_response('Nur Kunden können Bestellungen erstellen.')

       offer_detail = self.get_offer_detail_from_request(request.data)
       if not offer_detail:
           return self.bad_request_response('Das Feld "offer_detail_id" ist erforderlich.')

       order_data = self.prepare_order_data(request.user, offer_detail)
       return self.create_order(order_data)
 
 
    def is_customer(self, user):
     return user.type == 'customer'
    

    def forbidden_response(self, message):
       return Response({'detail': message}, status=status.HTTP_403_FORBIDDEN)


    def bad_request_response(self, message):
       return Response({'detail': message}, status=status.HTTP_400_BAD_REQUEST)
    

    def get_offer_detail_from_request(self, data):
       offer_detail_id = data.get('offer_detail_id')
       if not offer_detail_id:
           return None
       return get_object_or_404(OfferDetail, id=offer_detail_id)

    
    def prepare_order_data(self, customer_user, offer_detail):
       return {
        "customer_user": customer_user.id,
        "business_user": offer_detail.offer.user.id,
        "title": offer_detail.title,
        "revisions": offer_detail.revisions,
        "delivery_time_in_days": offer_detail.delivery_time_in_days,
        "price": offer_detail.price,
        "features": offer_detail.features,
        "offer_type": offer_detail.offer_type,
        "status": "in_progress",
    }


    def create_order(self, order_data):
       serializer = OrderSerializer(data=order_data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def partial_update(self, request, pk=None):
        """
        PATCH /orders/{id}/
        Only updates the status of an order.
        """
        queryset = self.get_queryset()
        order = get_object_or_404(queryset, pk=pk)

        status_update = request.data.get("status")
        if not status_update:
            return Response(
                {"detail": "Das Feld 'status' ist erforderlich."},
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_status_choices = [choice[0] for choice in Order.STATUS_CHOICES]
        if status_update not in valid_status_choices:
            return Response(
                {"detail": f"Ungültiger Status. Zulässige Werte sind: {', '.join(valid_status_choices)}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = status_update
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def retrieve(self, request, pk=None):
        """
        GET /orders/{id}/
        Retrieve the details of a specific order by its ID.
        """
        queryset = self.get_queryset()
        order = get_object_or_404(queryset, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class OrderCountView(APIView):
    """
    API endpoint to get the count of in-progress orders for a business user.
    """
    def get(self, request, business_user_id):
        business_user = get_object_or_404(CustomUser, id=business_user_id, type='business')
        order_count = Order.objects.filter(business_user=business_user, status='in_progress').count()
        
        return Response({"order_count": order_count}, status=status.HTTP_200_OK)
    

class CompletedOrderCountView(APIView):
    """
    API endpoint to get the count of completed orders for a business user.
    """
    def get(self, request, business_user_id):
        try:
            business_user = CustomUser.objects.get(id=business_user_id, type='business')
        except CustomUser.DoesNotExist:
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)
        
        order_count = Order.objects.filter(business_user=business_user, status='completed').count()
        return Response({"completed_order_count": order_count}, status=status.HTTP_200_OK)