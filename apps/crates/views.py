from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


from .serializers import CrateSerializer
from .models import Crate
from utils.permissions import IsProfileComplete


tags=["Crates"]

class CratesListCreateView(APIView, PageNumberPagination):
    serializer_class = CrateSerializer
    permission_classes = [IsProfileComplete]

    @extend_schema (
        summary="Retreive crates",
        description= "This endpoint retreives all crates",
        tags=tags
    )
    def get(self, request):
        crates = Crate.objects.all()
        
        self.page_size = 20
        paginated_queryset = self.paginate_queryset(crates, request, view=self)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)
    

    @extend_schema(
        tags=tags,
        summary="Create a new contact",
        description="This endpoint creates a new contact for the authenticated user.",
        request=CrateSerializer,
        responses={201: CrateSerializer},
        examples=[
            OpenApiExample(
                name="Create Contact Example",
                value={
                    "name": "SEN 308"
                },
                description="Example request body for creating a crate.",
            )
        ],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        user = request.user
        if serializer.is_valid():
            serializer.save(owner=user, school=user.school)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        # Override to set custom permissions for different HTTP methods
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return super().get_permissions()
 

class CrateDetailView(APIView):
    serializer_class = CrateSerializer

    @extend_schema (
        tags=tags,
        summary="Retreive a crate",
        description= "This endpoint retreives a specific crate using its id"
        
    )
    def get(self, request, id):
        crate = Crate.objects.prefetch_related("crate_materials").get(id=id)
        materials = crate.crate_materials

        serializer = self.serializer_class(crate)
        return Response({"Data":serializer.data})
    
    @extend_schema(
            tags=tags,
            summary="update a crate info",
            description="this endpoint is for updatuing crates info"
    )
    def put(self, request, id):
    
        crate = Crate.objects.get(id=id)
        owner = crate.owner
        serializer = self.serializer_class(crate, data=request.data)
        if serializer.is_valid(raise_exception=True):
            if owner == self.request.user:
                serializer.save()
                return Response({"success": "Crate updated successfully"})
            return Response({"error":"You have to be the owner to edit this crate"})
        return Response({"error": "Crate could not be updated"}, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
            tags=tags,
            summary="delete a crate",
            description="this endpoint deletes a crate"
    )
    def delete(self, request, id):
        crate = Crate.objects.get(id=id)
        owner = crate.owner
        #only the owner of a crate is able to delete
        if owner == self.request.user:
            crate.delete()
            return Response({"Success":"crate already deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error":"You have to be the owner to delete this crate"})

    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == "DELETE":
            return [IsAuthenticated(), IsProfileComplete()]
        return super().get_permissions() 

