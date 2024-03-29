
from .models import Material, Course
from .serializers import (
                    MaterialSerializer, 
                    CreateMaterialSerializer, 
                    CourseSerializer
                )

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema


tags = ["Course Materials"]

class MaterialsListCreateAPIView(APIView):
    serializer_class = MaterialSerializer
    post_serializer = CreateMaterialSerializer

    @extend_schema(
        tags=tags,
        summary="Get Materials",
        description="This endpoint should return materials from a user's school"
    )
    def get(self, request):
        materials = Material.objects.all()
        serializer = self.serializer_class(materials, many=True)
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)

    @extend_schema(
        tags=tags,
        summary="Upload a Material",
        description="This endpoint upoads a material to google drive",
        request=CreateMaterialSerializer,
        responses={"200": CreateMaterialSerializer},
    
    )
    def post(self, request):
        user = request.user
        context = {
            "request":request,
            "user":user,
            "school":user.school
        }
        serializer = self.post_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        course = serializer.validated_data["course"]
        
        serializer.save()

        return Response({"data":serializer.data}, status=status.HTTP_201_CREATED)


class CreateCourseAPIView(APIView):
    serializer_class= CourseSerializer

    def post(self, request):
        context = {
            "school":request.user.school
        }
        serializer = self.serializer_class(data = request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

