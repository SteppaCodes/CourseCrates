from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import status

from .serializers import (
    CompleteProfileSerializer,
    UserInfoSerializer
    )
from apps.schools.models import School
from apps.accounts.models import User


tags = ["Profiles"]


class CompleteProfileView(APIView):
    serializer_class = CompleteProfileSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
            tags=tags,
            summary= 'Complete Profile'
    )
    def put(self, request):
        user = request.user
        serializer= self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get all validated data inputs
        school_dict = serializer.validated_data.get('school')
        school = school_dict.get('school')
        level = serializer.validated_data['level']

        serializer.save(school=school, level=level, is_profile_complete=True)

        return Response(serializer.data)


class UserProfileAPIView(APIView):
    serializer_class = UserInfoSerializer

    @extend_schema(
            tags=tags,
            summary= 'User Profile',
            description="""
                This endpoint returns the user's profile - full name, display name,
                avatar, email, number of crates, number of subscribers, number of users subscribed to
            """
    )
    def get(self, request, slug):
        try:
            user = User.objects.prefetch_related("user_crates").get(slug=slug)
            serializer = UserInfoSerializer(user)
            return Response({"data": serializer.data})
        except User.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
