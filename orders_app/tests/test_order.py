from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class OrderViewSetTest(APITestCase):
    def setUp(self):
         self.user_model = get_user_model()
         self.user1 = self.user_model.objects.create_user(username="user1", password="password123")
         self.token = Token.objects.create(user=self.user1)
         self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

         self.order_url = reverse("orders.list-list")
