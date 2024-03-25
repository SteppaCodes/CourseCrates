from django.db.models import Q 

from . models import School
from .serializers import SchoolSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

tags = ["Schools"]

class CreateSchool(APIView):
    serializer_class = SchoolSerializer

    @extend_schema(
            tags=tags,
            summary='Create School',
            description="This endpoint creates a school"
    )
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class SchoolsListView(APIView):
    serializer_class = SchoolSerializer

    @extend_schema(
            tags=tags,
            summary='List all schools',
            description="This endpoint lists all schools"
    )
    def get(self, request):
        query = request.GET.get("query")
        if query ==None:
            query = ''
        schools = School.objects.filter(
            Q(name__icontains=query)|Q(abv__icontains=query)
            )
        
        serializer = self.serializer_class(schools, many=True)
        return Response({"schools":serializer.data})