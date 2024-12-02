from django.urls import path, include
from orders_app.api.views import OrderViewSet
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

router= routers.SimpleRouter()
router.register(r'orders', OrderViewSet, basename='orders.list')

urlpatterns = [
    path('', include(router.urls))


]