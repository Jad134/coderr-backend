from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from offers_app.models import Offer, OfferDetail
from rest_framework.authtoken.models import Token

class OfferViewSetTest(APITestCase):
    def setUp(self):
        """
        Set up users, offers, and offer details for testing.
        """
        self.user_model = get_user_model()  # Dynamisch das benutzerdefinierte Modell laden
        self.user1 = self.user_model.objects.create_user(username="user1", password="password123")
        self.user2 = self.user_model.objects.create_user(username="user2", password="password123")
        self.token = Token.objects.create(user=self.user1)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.offer_url = reverse("offer-list")
        self.offer1 = Offer.objects.create(
            user=self.user1,
            title="Offer 1",
            description="Description 1",
            min_price=10.00,
            min_delivery_time=3
        )
        self.offer2 = Offer.objects.create(
            user=self.user2,
            title="Offer 2",
            description="Description 2",
            min_price=20.00,
            min_delivery_time=5
        )
        self.offers_url = reverse("offer-list")
        self.offer_delete_url = reverse("offer-detail", kwargs={"pk": self.offer1.pk})


    def test_list_all_offers(self):
        """
        Tests listing all offers.
        """
        response = self.client.get(self.offers_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["title"], "Offer 1")
        self.assertEqual(response.data["results"][1]["title"], "Offer 2")


    def test_list_offers_filtered_by_creator(self):
        """
        Tests filtering offers by creator ID.
        """
        response = self.client.get(self.offers_url, {"creator_id": self.user1.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Offer 1")
        self.assertEqual(response.data["results"][0]["user"], self.user1.id)


    def test_create_offer_success(self):
        """
        Tests successful creation of an offer.
        """
        data = {
            "title": "New Offer",
            "description": "New description",
            "min_price": 50.00,
            "min_delivery_time": 7,
            "details": [
                {
                    "offer_type": "basic",
                    "title": "Basic Plan",
                    "revisions": 2,
                    "delivery_time_in_days": 3,
                    "price": 100.00,
                    "features": ["Feature 1", "Feature 2"]
                },
                  {
                    "offer_type": "standard",
                    "title": "Basic Plan",
                    "revisions": 2,
                    "delivery_time_in_days": 3,
                    "price": 100.00,
                    "features": ["Feature 1", "Feature 2"]
                },
                  {
                    "offer_type": "premium",
                    "title": "Basic Plan",
                    "revisions": 2,
                    "delivery_time_in_days": 3,
                    "price": 100.00,
                    "features": ["Feature 1", "Feature 2"]
                }
            ]
        }

        response = self.client.post(self.offers_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Offer")
        self.assertEqual(response.data["user"], self.user1.id)


    def test_creator_can_delete_offer(self):
        """Test that the creator of an offer can delete it."""
        response = self.client.delete(self.offer_delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Offer.objects.filter(id=self.offer1.id).exists())


    def test_filter_offers_by_min_price(self):
        """
        Tests filtering offers by minimum price.
        """
        response = self.client.get(self.offers_url, {"min_price": 15})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Offer 2")