from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class ReviewTests(APITestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.customer_user = self.user_model.objects.create_user(username="customer", password="password123", type="customer")
        self.business_user = self.user_model.objects.create_user(username="business", password="password123", type="business")

        self.token = Token.objects.create(user=self.customer_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.review_url = reverse("reviews-list")


    def test_create_review(self):
        """
        Test create an Review
        """

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_1.key)
        url = reverse('base-info', kwargs={'pk': self.user_1.pk})