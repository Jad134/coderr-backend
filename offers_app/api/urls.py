from django.urls import path, include
from rest_framework import routers
from offers_app.api.views import OfferViewSet

router= routers.SimpleRouter()
router.register(r'offers', OfferViewSet, basename='offer')

urlpatterns = [
    path('', include(router.urls)),


]