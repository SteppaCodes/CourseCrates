from rest_framework.permissions import BasePermission
from rest_framework.response import Response 
from rest_framework.exceptions import PermissionDenied

class IsProfileComplete(BasePermission):
    def has_permission(self, request, view):
        # Allow access to the view for all anonymous users and 
        #authorized users that have completed their profile
        user = request.user
        if user.is_authenticated and not user.is_profile_complete:
            raise PermissionDenied(detail="Please complete your profile setup")
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and user.is_profile_complete