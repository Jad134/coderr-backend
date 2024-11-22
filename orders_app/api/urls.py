from django.urls import path, include
from user_auth_app.api.views import RegisterUserView, LoginView, UserViewSet
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

router= routers.SimpleRouter()
router.register()

urlpatterns = [
    path('', include(router.urls)),


]