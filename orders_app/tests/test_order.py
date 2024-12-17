from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user1 = self.user_model.objects.create_user(username="user1", password="password123", type='customer')
        self.user2 = self.user_model.objects.create_user(username="user2", password="password123")
        self.token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.order_url = reverse("orders.list-list")

        self.offer = Offer.objects.create(
            user=self.user2,  
            title="Sample Offer",
            description="This is a sample offer.",
            min_price=Decimal('199.99'),
            min_delivery_time=5
        )

        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,  
            offer_type='premium',
            title="Sample Offer Detail",
            revisions=3,
            delivery_time_in_days=5,
            price=Decimal('199.99'),
            features=['feature1', 'feature2'],
        )

        self.order1 = Order.objects.create(
            customer_user=self.user1,
            business_user=self.user2,
            title="Order Title",
            revisions=3,
            delivery_time_in_days=5,
            price=Decimal('99.99'),
            features=['feature1', 'feature2'],
            offer_type='premium',
            status='in_progress'
        )

        self.order2 = Order.objects.create(
            customer_user=self.user1,
            business_user=self.user2,
            title="Another Order Title",
            revisions=2,
            delivery_time_in_days=7,
            price=Decimal('149.99'),
            features=['feature3', 'feature4'],
            offer_type='standard',
            status='completed'
        )


    def test_order_creation(self):

     order_data = {
        "customer_user": self.user1.id,
        "business_user": self.user2.id,
        "title": self.offer_detail.title, 
        "revisions": 1,
        "delivery_time_in_days": 10,
        "price": Decimal('199.99'),
        "features": ["feature5"],
        "offer_type": "basic",
        "status": "in_progress",
        "offer_detail_id": self.offer_detail.id  
    }

     response = self.client.post(self.order_url, order_data, format="json")


     self.assertEqual(response.status_code, 201)


     self.assertEqual(response.data['title'], "Sample Offer Detail")
     self.assertEqual(response.data['price'], "199.99")
     self.assertEqual(response.data['status'], "in_progress")


    def test_list_orders(self):
        """
        Test the /List method
        """
        response = self.client.get(reverse("orders.list-list"))  
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)  
        self.assertEqual(response.data[0]["title"], "Order Title")
