from django.urls import path, include
from orders_app.api.views import OrderCountView, OrderViewSet, CompletedOrderCountView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

router= routers.SimpleRouter()
router.register(r'orders', OrderViewSet, basename='orders.list')

urlpatterns = [
    path('', include(router.urls)),
    path('order-count/<int:business_user_id>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/', CompletedOrderCountView.as_view(), name='completed-order-count')


]