from rest_framework import serializers
from .models import School

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


    #check if school exists or create a new one
    def validate(self, attrs):
        name = attrs.get('name')
        abv = attrs.get('abv')

        school = School.objects.filter(name=name).first()
        if school:
            return {'school': school, 'created': False}
        else:
            new_school = School.objects.create(name=name, abv=abv)
            return {'school': new_school, 'created': True}

        return super().validate(attrs)
