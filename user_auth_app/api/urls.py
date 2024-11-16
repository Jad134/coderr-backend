from django.urls import path
from user_auth_app.api.views import RegisterUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
]