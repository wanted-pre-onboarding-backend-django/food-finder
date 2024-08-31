# restaurant/serializers.py

from rest_framework import serializers
from restaurant.models import Restaurant


class RestaurantDetailSerializer(serializers.ModelSerializer):
    """맛집 상세 정보 시리얼라이저"""

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "name",
            "category",
            "status",
            "road_addr",
            "lot_addr",
            "lat",
            "lon",
            "rating",
            "province",
            "reviews",
        ]
