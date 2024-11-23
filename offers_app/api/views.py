from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from offers_app.api.serializers import OfferDetailSerializer, OfferSerializer
from offers_app.models import Offer, OfferDetail
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination


class OfferPagination(PageNumberPagination):
    page_size = 6 # Anzahl der Einträge pro Seite

class OfferViewSet(viewsets.ViewSet):
    pagination_class = OfferPagination

    def create(self, request):
        """Create an new offer."""
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        queryset = Offer.objects.prefetch_related('details')
        creator_id = request.query_params.get('creator_id')
        if creator_id:
            queryset = queryset.filter(user_id=creator_id)

        min_price = request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(min_price__gte=min_price)

        max_delivery_time = request.query_params.get('max_delivery_time')
        if max_delivery_time:
            queryset = queryset.filter(min_delivery_time__lte=max_delivery_time)
            
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = OfferSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def partial_update(self, request, pk=None):
        queryset = Offer.objects.all()
        offer = get_object_or_404(queryset, pk=pk)  
        serializer = OfferSerializer(offer, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        queryset = Offer.objects.all()
        offer = get_object_or_404(queryset, pk=pk)
        serializer = OfferSerializer(offer)
        return Response(serializer.data)

    
class OfferDetailViewSet(viewsets.ViewSet):
    queryset = OfferDetail.objects.all()
    def retrieve(self, request, pk=None):
        detail = get_object_or_404(self.queryset, pk=pk)
        serializer = OfferDetailSerializer(detail)
        return Response(serializer.data)