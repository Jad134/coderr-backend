from rest_framework import serializers

from user_auth_app.models import CustomUser

class UserSerializer(serializers.ModelSerializer):

   
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password',  'type']
        extra_kwargs = {
            'password': {'write_only': True},  
        }