from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from restaurant.models import Restaurant


class RestaurantListSerializer(ModelSerializer):
    """맛집 리스트 시리얼라이저"""

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "category",
            "name",
            "status",
            "road_addr",
            "lot_addr",
            "lat",
            "lon",
            "rating",
        ]
