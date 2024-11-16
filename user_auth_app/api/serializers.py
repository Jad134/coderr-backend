from rest_framework import serializers

from user_auth_app.models import User

class UserSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
   
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True},  
        }