from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user_auth_app.models import CustomUser
from rest_framework.authtoken.models import Token

class RegisterTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')

    def test_register_success(self):
       """
       Testet eine erfolgreiche Benutzerregistrierung.
       """

       data = {
           "username": "JaneDoe",
           "email": "janedoe@example.com",
           "password": "securepassword123",  
           "repeated_password": "securepassword123",  
           "type": "customer",
       }

       response = self.client.post(self.register_url, data, format='json')
       self.assertEqual(response.status_code, status.HTTP_201_CREATED)

       user = CustomUser.objects.filter(username="JaneDoe").first()
       self.assertIsNotNone(user)
       self.assertEqual(user.email, "janedoe@example.com")
       self.assertEqual(user.type, "customer")
       self.assertTrue(user.check_password("securepassword123"))  # Überprüfen, ob das Passwort korrekt gehasht wurde



    def test_register_password_mismatch(self):
        """
        Testet, ob die Registrierung fehlschlägt, wenn die Passwörter nicht übereinstimmen.
        """
        data = {
            "username": "JaneDoe",
            "email": "janedoe@example.com",
            "password": "securepassword123",
            "repeated_password": "differentpassword",
            "type": "customer",
        }

        response = self.client.post(self.register_url, data)

        # Teste, ob die Antwort einen Fehler zurückgibt
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Passwörter stimmen nicht überein.", response.data.get("error", ""))

    
