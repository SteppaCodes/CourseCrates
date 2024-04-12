from rest_framework import serializers

from .models import Crate
from apps.accounts.serializers import UserSerializer

class CreateCrateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Crate
        fields = [
            'slug',
            'name',
            'owner',
            'school',
            # 'material_count'
        ]

        read_only_fields = ["owner", "school"]


class CrateDetailSerializer(serializers.ModelSerializer):
    material_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Crate
        fields = [
            "name",
            "slug",
            "owner",
            "material_count"
        ]

    read_only_fields = ["owner"]

    def get_material_count(self, obj) -> int:
        return obj.crate_materials.count()    
