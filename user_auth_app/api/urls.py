from django.urls import path, include
from user_auth_app.api.views import RegisterUserView, LoginView, UserViewSet
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

router= routers.SimpleRouter()
router.register(r'profile', UserViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('registration/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

]