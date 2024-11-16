from django.shortcuts import render
from user_auth_app.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer


class RegisterUserView(APIView):
    """
    View zur Benutzerregistrierung.
    """
    def post(self, request, *args, **kwargs):
        # Extrahiere Daten aus dem Request
        data = request.data
        password = data.get('password')
        repeated_password = data.get('repeated_password')

        # Überprüfen, ob Passwörter übereinstimmen
        if password != repeated_password:
            return Response(
                {"error": "Passwörter stimmen nicht überein."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Entferne repeated_password vor dem Erstellen des Benutzers
        data.pop('repeated_password', None)

        # Überprüfe und speichere Benutzer mit einem Serializer
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save(password)  
            return Response(
                {"message": "Erfolgreich registriert."},
                status=status.HTTP_200_OK
            )

        # Rückgabe bei ungültigen Eingaben
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)