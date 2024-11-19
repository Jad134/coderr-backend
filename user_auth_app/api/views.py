import copy
from django.shortcuts import render
from user_auth_app.models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model



class RegisterUserView(APIView):
    """
    View zur Benutzerregistrierung.
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
        Überprüft, ob die Passwörter übereinstimmen und ob sie nicht leer sind.
        Gibt eine Response zurück, wenn ein Fehler gefunden wird, andernfalls None.
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

        return None  # Keine Fehler, also Rückgabe von None
    
    def create_user(self, data):
        User = get_user_model()
        password = data.pop('password', None)
        user = User(**data)

        if password:
            user.set_password(password)
    
        user.save()

        return user
    

class LoginView(ObtainAuthToken):
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
