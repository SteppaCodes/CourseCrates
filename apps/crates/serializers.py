from rest_framework import serializers

from .models import Crate
from apps.accounts.serializers import UserSerializer

class CrateSerializer(serializers.ModelSerializer):
    # material_count = serializers.SerializerMethodField(read_only=True)
    owner = serializers.CharField(read_only=True)
    school = serializers.CharField(read_only=True)
    
    class Meta:
        model = Crate
        fields = [
            'id',
            'name',
            'owner',
            'school',
            # 'material_count'
        ]

    # def get_material_count(self, obj) -> int:
    #     if obj.crate_materials.all():
    #         return obj.crate_materials.count()    