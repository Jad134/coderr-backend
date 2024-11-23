from rest_framework import status
from rest_framework import viewsets
from offers_app.api.serializers import OfferSerializer
from offers_app.models import Offer
from rest_framework.response import Response

class OfferViewSet(viewsets.ViewSet):
    
    def create(self, request):
        """Erstellt ein neues Angebot."""
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Aktuellen Benutzer als Ersteller setzen
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)