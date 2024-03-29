from rest_framework import serializers

from .models import Material, Course

from django.urls import reverse


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model= Course
        fields  = [
            "id",
            "code",
            "title",
        ]

        read_only_fields = ["id"]

    def validate(self, attrs):
        code = attrs.get('code')
        title = attrs.get('title')
        school = self.context["school"]

        course = Course.objects.filter(code=code).first()
        if course:
            return {'course': course, 'created': False}
        else:
            new_course = Course.objects.create(code=code, title=title, school=school)
            return {'course': new_course, 'created': True}


class MaterialSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Material
        fields = [
            'name',
            'file',
            'category',
            'crate',
            'size',
            'owner',
            'school',
            'level',
        ]


class CreateMaterialSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    size = serializers.SerializerMethodField()
    class Meta: 
        model = Material
        fields = [
            'name',
            'file',
            'category',
            'course',
            'crate',
            'size',
            'owner',
            'school',
            'level',
            'created_at',
            'updated_at'
        ]

        read_only_fields = ['owner', 'school', 'created_at', 'updated_at']
        

    def get_size(self, obj):
        file_size = 0
        if obj.file and hasattr(obj.file, "size"):
            file_size = obj.file.size
        return file_size
    
    def validate(self, attrs):
        course= attrs.get("course")
        if course:
            code = course.get('course_code')
            title = course.get('course_title')
        
            view_name = "create-course"

            reverse(view_name, kwargs={'code':code, 'title':title})
            
        validated_data = super().validate(attrs)
        return validated_data

    def create(self, validated_data):
        course_data = validated_data.pop('course', None)
        material = Material.objects.create(
            school=self.context['school'],
            owner=self.context['user'],
            **validated_data
        )

        if course_data:
            course = course_data["course"]
            material.course = course
            material.save()

        return material

