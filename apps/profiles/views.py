from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .serializers import (
    CompleteProfileSerializer
    )
from apps.schools.models import School
from apps.accounts.models import User

tags = ["Accounts Settings"]

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


