from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from user_auth_app.models import Review


class ReviewTests(APITestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.customer_user = self.user_model.objects.create_user(username="customer", password="password123", type="customer")
        self.business_user = self.user_model.objects.create_user(username="business", password="password123", type="business")

        self.token = Token.objects.create(user=self.customer_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.review_url = reverse("reviews-list")


    def test_create_review_success(self):
        """
        Test that a customer can create a review for a business user.
        """
        payload = {
            "business_user": self.business_user.id,
            "rating": 5,
            "description": "Great service!"
        }
        
        response = self.client.post(self.review_url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().rating, 5)
        self.assertEqual(Review.objects.first().description, "Great service!")


    def test_create_duplicate_review(self):
        """
        Test that a customer cannot create multiple reviews for the same business user.
        """
        # Create an initial review
        Review.objects.create(
            reviewer=self.customer_user,
            business_user=self.business_user,
            rating=5,
            description="Great service!"
        )
        
        payload = {
            "business_user": self.business_user.id,
            "rating": 4,
            "description": "Good, but not perfect!"
        }
        
        response = self.client.post(self.review_url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["detail"], "You have already reviewed this business user.")
        self.assertEqual(Review.objects.count(), 1) 


    def test_create_review_unauthenticated(self):
        """
        Test that unauthenticated users cannot create a review.
        """
        self.client.credentials()
        
        payload = {
            "business_user": self.business_user.id,
            "rating": 5,
            "description": "Great service!"
        }
        
        response = self.client.post(self.review_url, payload, format="json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Review.objects.count(), 0)


    def test_create_review_invalid_business_user(self):
        """
        Test that creating a review for a non-existent business user returns an error.
        """
        payload = {
            "business_user": 9990,  # Non-existent ID
            "rating": 5,
            "description": "Great service!"
        }
        
        response = self.client.post(self.review_url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.data)
        self.assertEqual(Review.objects.count(), 0)