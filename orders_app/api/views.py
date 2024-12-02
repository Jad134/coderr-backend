from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from orders_app.api.serializers import OrderSerializer
from orders_app.models import Order
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination


class OrderViewSet(viewsets.ViewSet):
    queryset = Order.objects.all()


    def list(self, request):
        """
        Get order list with queryset for filter methods in Frontend Code e.g only show own offers with creator_id
        """
        queryset = self.queryset 
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)