from rest_framework import serializers

from user_auth_app.models import CustomUser

class UserSerializer(serializers.ModelSerializer):

   
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password',  'type','first_name','last_name', 'profile_picture', 'location', 'tel', 'description', 'working_hours']
        extra_kwargs = {
            'password': {'write_only': True},  
        }