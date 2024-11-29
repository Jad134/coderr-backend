import copy
from django.shortcuts import render,get_object_or_404
from user_auth_app.models import CustomUser, Review
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BusinessUserSerializer, CustomerUserSerializer, ReviewSerializer, UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCustomer




class RegisterUserView(APIView):
    """
    User registration view.
    """
    def post(self, request, *args, **kwargs):

        data = request.data.copy()
        password = data.get('password')
        repeated_password = data.get('repeated_password')

        password_check_result = self.check_password(password, repeated_password)
        if password_check_result:
            return password_check_result
        data.pop('repeated_password', None)

        try:
            user = self.create_user(data)
            return Response(
                {"message": "Erfolgreich registriert.", "user_id": user.id},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def check_password(self, password, repeated_password):
        """
        Checks whether the passwords match and whether they are not empty.
        Returns a Response if an error is found, otherwise None.
        """

        if not password or not repeated_password:
            return Response(
                {"error": "Passwort und Wiederholung des Passworts sind erforderlich."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if password != repeated_password:
            return Response(
                {"error": "Passwörter stimmen nicht überein."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return None  
    
    def create_user(self, data):
        User = get_user_model()
        password = data.pop('password', None)
        user = User(**data)

        if password:
            user.set_password(password)
    
        user.save()

        return user
    

class LoginView(ObtainAuthToken):
    """
    User registration view.
    """
    def post(self, request, *args, **kwargs):

        username = request.data.get('username', '').lower()

        try:
            user = CustomUser.objects.get(username__iexact=username)  # 'iexact' for case-insensitive comparison
        except CustomUser.DoesNotExist:
            return Response({"error": "Benutzername oder Passwort ungültig."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(request.data.get('password')):
            return Response({"error": "Benutzername oder Passwort ungültig."}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "type": user.type, 
        }, status=status.HTTP_200_OK)
    
class UserViewSet(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        user= get_object_or_404(self.queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response (serializer.data)
    
    def partial_update(self, request, pk=None):
        user = request.user  

        if str(user.pk) != str(pk):
            return Response({'error': 'Nicht berechtigt, dieses Profil zu bearbeiten.'}, status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(self.queryset, pk=user.pk)
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BusinessUserViewSet(viewsets.ViewSet):
    def list(self, request):
        business_users = CustomUser.objects.filter(type=CustomUser.BUSINESS) 
        serializer = BusinessUserSerializer(business_users, many=True)
        
        return Response(serializer.data)

    
class CustomerUserViewSet(viewsets.ViewSet):
    def list(self, request):
        customer_users = CustomUser.objects.filter(type=CustomUser.CUSTOMER)
        serializer = CustomerUserSerializer(customer_users, many=True)

        return Response(serializer.data)

    


class ReviewViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for get or creating reviews.
    """
    
    queryset = Review.objects.all()

    def retrieve(self, request, pk=None):
        review= get_object_or_404(self.queryset, pk=pk)
        serializer = ReviewSerializer(review)
        return Response (serializer.data)

    def list(self, request):
        """
        GET /reviews/
        List reviews with optional filters and ordering.
        """
        queryset = self.get_filtered_reviews(request)
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        POST /reviews/
        Create a review for a business user. Only customers can create reviews.
        """
        self.permission_classes = [IsAuthenticated, IsCustomer]
        business_user = self.get_valid_business_user(request)
        if isinstance(business_user, Response):
            return business_user
        if self.review_already_exists(business_user, request.user):
            return Response(
                {'detail': 'You have already reviewed this business user.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return self.save_review(request, business_user)

    def get_filtered_reviews(self, request):
        queryset = Review.objects.all()
        business_user_id = request.query_params.get('business_user_id')
        if business_user_id:
            queryset = queryset.filter(business_user_id=business_user_id)
        reviewer_id = request.query_params.get('reviewer_id')
        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)
        ordering = request.query_params.get('ordering', '-updated_at')
        if ordering in ['rating', '-rating', 'updated_at', '-updated_at']:
            queryset = queryset.order_by(ordering)
        return queryset

    def get_valid_business_user(self, request):
        business_user_id = request.data.get('business_user_id')
        if not business_user_id:
            return Response(
                {'detail': 'business_user_id is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            return CustomUser.objects.get(id=business_user_id, type='business')
        except CustomUser.DoesNotExist:
            return Response(
                {'detail': 'Invalid business_user_id.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def review_already_exists(self, business_user, reviewer):
        return Review.objects.filter(
            business_user=business_user, reviewer=reviewer
        ).exists()

    def save_review(self, request, business_user):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(business_user=business_user, reviewer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
