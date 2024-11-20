from django.urls import path
from user_auth_app.api.views import RegisterUserView, LoginView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('registration/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

]