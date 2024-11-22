from rest_framework import serializers

from user_auth_app.models import CustomUser

class UserSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = CustomUser
        fields = ['user','username', 'email', 'password',  'type','first_name','last_name', 'file', 'location', 'tel', 'description', 'working_hours','created_at']
        extra_kwargs = {
            'password': {'write_only': True},  
        }