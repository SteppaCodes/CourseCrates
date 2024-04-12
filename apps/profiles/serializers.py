from django.urls import reverse

from rest_framework import serializers
import requests

from apps.accounts.models import User
from apps.schools.serializers import SchoolSerializer
from apps.schools.models import School
from apps.crates.serializers import CrateDetailSerializer


class CompleteProfileSerializer(serializers.ModelSerializer):
    school = SchoolSerializer()
    class Meta:
        model = User
        fields = (
            'first_name', 
            'last_name',
            'display_name', 
            'email', 
            'avatar',
            'school', 
            'level'
            )

    #send the school info to the create school view 
    def validate(self, attrs):
        school = attrs.get('school')
        #get the name and abv from the serializer
        school_name =  school.get('name')
        abv = school.get('abv')
        view_name = "create_school"

        #send the parameters to the createschool view
        reverse(view_name, kwargs={'name':school_name, 'abv':abv})
        
        validated_attrs = super().validate(attrs)
        return validated_attrs


class UserInfoSerializer(serializers.ModelSerializer):
    crates_count = serializers.SerializerMethodField(read_only=True)
    user_crates = CrateDetailSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'full_name',
            'display_name',
            'email',
            'avatar',
            'crates_count',
            'user_crates'
        ]

    def get_crates_count(self, obj) -> int:
        user_crates = obj.user_crates.count()        
        return user_crates
    
