from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from province.models import Province


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = [
            "city",
            "lat",
            "lon",
        ]
