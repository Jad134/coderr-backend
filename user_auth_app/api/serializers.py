from rest_framework import serializers
from user_auth_app.models import CustomUser,Review

class UserSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = CustomUser
        fields = ['user','username', 'email', 'password',  'type','first_name','last_name', 'file', 'location', 'tel', 'description', 'working_hours','created_at']
        extra_kwargs = {
            'password': {'write_only': True},  
        }

class BusinessUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {
            "pk": obj.id,
            "username": obj.username,
            "first_name": obj.first_name,
            "last_name": obj.last_name
        }

    class Meta:
        model = CustomUser
        fields = ['user', 'file', 'location', 'tel', 'description', 'working_hours', 'type']


class CustomerUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {
            "pk": obj.id,
            "username": obj.username,
            "first_name": obj.first_name,
            "last_name": obj.last_name
        }

    class Meta:
        model = CustomUser
        fields = ['user', 'file', 'created_at', 'type']


class ReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']