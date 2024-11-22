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
       Tests successful user registration.
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
       self.assertTrue(user.check_password("securepassword123")) 


    def test_register_password_mismatch(self):
        """
        Tests whether registration fails if passwords do not match.
        """
        data = {
            "username": "JaneDoe",
            "email": "janedoe@example.com",
            "password": "securepassword123",
            "repeated_password": "differentpassword",
            "type": "customer",
        }

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Passwörter stimmen nicht überein.", response.data.get("error", ""))


class LoginViewTest(APITestCase):

    def setUp(self):
        """
        Set up a test user and the login URL.
        """
        self.login_url = reverse('login')  
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='securepassword123',
            type='customer'
        )

    def test_login_success(self):
        """
        Test a successful login with valid credentials.
        """
        data = {
            "username": "testuser",
            "password": "securepassword123"
        }

        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)  # Sicherstellen, dass user_id vorhanden ist
        self.assertEqual(response.data.get('user_id'), self.user.id)  # Absichern gegen fehlenden Key


    def test_login_failure_missing_fields(self):
       """
       Test login failure due to missing username or password.
       """
       data = {
         "username": "testuser"
       }

       response = self.client.post(self.login_url, data, format='json')

       self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

       self.assertNotIn('username', response.data) 



    
