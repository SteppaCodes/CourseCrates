from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from .serializers import CrateSerializer
from .models import Crate
from utils.permissions import IsProfileComplete
from apps.schools.models import School
from apps.accounts.models import GuestUser


tags=["Crates"]

class CratesListCreateAPIView(APIView, PageNumberPagination):
    serializer_class = CrateSerializer
    permission_classes = [IsProfileComplete]
    user = None

    @extend_schema (
        summary="Retrieve a paginated list of crates",
        description="""
                    This endpoint retrieves a paginated list of crates associated with the authenticated user's school. 
                    Unauthenticated users with a valid session key will be associated with a guest user for their school.
                """,
        tags=tags,
        parameters=[
        OpenApiParameter(
            name= "page",
            type=int,
            required=False,
            description="Page number (used for pagination)",
            ),
        ],
        responses={
            200: CrateSerializer(many=True),
            401: CrateSerializer,
        },
    )
    def get(self, request):
        self.user = request.user
        if not request.user.is_authenticated:
            session_key = request.session.session_key
            try:
                user = GuestUser.objects.get(session_key=session_key)
                self.user = user
            except GuestUser.DoesNotExist:
                return Response({"error":"Please login or signup"})

        crates = Crate.objects.filter(school=self.user.school)
        self.page_size = 20
        paginated_queryset = self.paginate_queryset(crates, request, view=self)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        tags=tags,
        summary="Create a new crate",
        description="""
                This endpoint creates a new crate associated with the authenticated user's school.
            """,
        request=CrateSerializer,
        responses={201: CrateSerializer},
        examples=[
            OpenApiExample(
                name="Create Crate Example",
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
            return [IsAuthenticated(), IsProfileComplete()]
        return super().get_permissions()


class CrateDetailView(APIView):
    serializer_class = CrateSerializer

    @extend_schema (
        tags=tags,
        summary="Retrieve a specific crate",
        description="""
            This endpoint retrieves a specific crate using its slug.

            - If the user is authenticated, the crate must belong to the user's school.
            - If the user is unauthenticated and provides a valid `school_id`:
                - The school with the provided ID is retrieved.
                - A guest user associated with the provided school and the user's session key is created (if it doesn't exist).
                - Access is granted only if the crate belongs to the retrieved school.
        """,
    )
    def get(self, request, slug, school_id=None):
        crate = Crate.objects.prefetch_related("crate_materials").get(slug=slug)
        materials = crate.crate_materials

        if school_id:
            id =  force_str(urlsafe_base64_decode(school_id))
            if not request.user.is_authenticated:
                school = get_object_or_404(School, id=id)
                session_key = request.session.session_key
                user, created = GuestUser.objects.get_or_create(session_key=session_key, school = school)
                 
        serializer = self.serializer_class(crate)
        return Response({"Data":serializer.data})
    
    @extend_schema(
            tags=tags,
            summary="Update a crate's information",
            description="""
                This endpoint updates a crate's attributes based on the provided data.

                - Only the owner of a crate can update its information.
                - All required fields for crate creation must be included in the request body.
            """,
    )
    def put(self, request, slug):
        crate = Crate.objects.get(slug=slug)
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
            summary="Delete a specific crate",
            description="""
                This endpoint permanently deletes the specified crate.
                - Only the crate's owner can perform the deletion.
                - Deletion is irreversible.
            """,
    )
    def delete(self, request, slug):
        crate = Crate.objects.get(slug=slug)
        owner = crate.owner

        if owner == self.request.user:
            crate.delete()
            return Response({"Success":"Crate deleted succesfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error":"You have to be the owner to delete this crate"})

    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == "DELETE":
            return [IsAuthenticated(), IsProfileComplete()]
        return super().get_permissions() 


class GenerateCrateShareLink(APIView):
    @extend_schema(
        tags=tags,
        summary="Generate a shareable link for a crate",
        description="""
            This endpoint generates a shareable link for a specific crate.
            - Authenticated users can share crates associated with their school.
            - Unauthenticated users with a valid session key can share crates associated with their school.
        """
    )
    def get(self, request, slug):
        user = request.user
        if  not request.user.is_authenticated:
            session_key = request.session.session_key
            try:
                user = GuestUser.objects.get(sseession_key=session_key)
            except GuestUser.DoesNotExist:
                return Response({"error":"You cannot share this crates, please login or sign up"})

        
        school_id = urlsafe_base64_encode(force_bytes(user.school.id))
        site = get_current_site(request).domain
        url = reverse('crate-detail', args=[slug, school_id])

        link = f"{request.scheme}://{site}{url}"

        return Response({"link":link})

