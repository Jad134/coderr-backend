from django.urls import path, include
from user_auth_app.api.views import RegisterUserView, LoginView, UserViewSet, BusinessUserViewSet, CustomerUserViewSet, ReviewViewSet
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

router= routers.SimpleRouter()
router.register(r'profile', UserViewSet, basename='profile')
router.register(r'profiles/business', BusinessUserViewSet, basename='business-user')
router.register(r'profiles/customer', CustomerUserViewSet, basename='customer-user')
router.register(r'reviews',ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('registration/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

]