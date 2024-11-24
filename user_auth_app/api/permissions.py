from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """
    Custom permission to allow only authenticated users with the 'customer' type to create reviews.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'