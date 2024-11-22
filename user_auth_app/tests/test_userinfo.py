from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user_auth_app.models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

class userPatchTest(APITestCase):
  
    def setUp(self):
        self.user_1 = get_user_model().objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123',
            first_name='John',
            last_name='Doe',
            type='business'
        )
        self.user_2 = get_user_model().objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password456',
            first_name='Jane',
            last_name='Smith',
            type='business'
        )

        self.token_1 = Token.objects.create(user=self.user_1)
        self.token_2 = Token.objects.create(user=self.user_2)

    def test_partial_update_success(self):
       self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_1.key)

       url = reverse('profile-detail', kwargs={'pk': self.user_1.pk})

       data = {
            'first_name': 'Updated John',
            'email': 'updatedjohn@example.com'
        }
       
       response = self.client.patch(url, data, format='json')

       self.assertEqual(response.status_code, status.HTTP_200_OK)
       self.assertEqual(response.data['first_name'], 'Updated John')
       self.assertEqual(response.data['email'], 'updatedjohn@example.com')
