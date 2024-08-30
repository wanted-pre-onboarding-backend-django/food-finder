from rest_framework import serializers
from province.models import Province


class ProvinceSerializer(serializers.ModelSerializer):
    city = serializers.CharField(max_length=50)
    lat = serializers.DecimalField(max_digits=9, decimal_places=6)
    lon = serializers.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        model = Province
        fields = [
            "city",
            "lat",
            "lon",
        ]
