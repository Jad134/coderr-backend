from rest_framework import serializers
from orders_app.models import Order

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

