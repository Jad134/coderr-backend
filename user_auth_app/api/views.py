import copy
from django.shortcuts import render,get_object_or_404
from user_auth_app.models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated




class RegisterUserView(APIView):
    """
    User registration view.
    """
    def post(self, request, *args, **kwargs):

        data = request.data.copy()
        password = data.get('password')
        repeated_password = data.get('repeated_password')

        password_check_result = self.check_password(password, repeated_password)
        if password_check_result:
            return password_check_result
        data.pop('repeated_password', None)

        try:
            user = self.create_user(data)
            return Response(
                {"message": "Erfolgreich registriert.", "user_id": user.id},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def check_password(self, password, repeated_password):
        """
        Checks whether the passwords match and whether they are not empty.
        Returns a Response if an error is found, otherwise None.
        """

        if not password or not repeated_password:
            return Response(
                {"error": "Passwort und Wiederholung des Passworts sind erforderlich."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if password != repeated_password:
            return Response(
                {"error": "Passwörter stimmen nicht überein."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return None  
    
    def create_user(self, data):
        User = get_user_model()
        password = data.pop('password', None)
        user = User(**data)

        if password:
            user.set_password(password)
    
        user.save()

        return user
    

class LoginView(ObtainAuthToken):
    """
    User registration view.
    """
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']  
            token, created = Token.objects.get_or_create(user=user)  


            
            return Response({
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "type": user.type,  
            }, status=status.HTTP_200_OK)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserViewSet(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        user= get_object_or_404(self.queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response (serializer.data)
    
    def partial_update(self, request, pk=None):
        # Verwende den authentifizierten Benutzer, um das Profil zu aktualisieren
        user = request.user  # Hier holen wir den authentifizierten Benutzer (durch Login-Token oder Session)

        # Stelle sicher, dass der Benutzer nur sein eigenes Profil bearbeitet
        if str(user.pk) != str(pk):
            return Response({'error': 'Nicht berechtigt, dieses Profil zu bearbeiten.'}, status=status.HTTP_403_FORBIDDEN)

        # Hole das Benutzerobjekt basierend auf der ID des authentifizierten Benutzers
        user = get_object_or_404(self.queryset, pk=user.pk)

        # Verwende den Serializer, um die Daten zu validieren und zu speichern
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()  # Speichern der geänderten Daten
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    