from rest_framework import serializers
from review.models import Review
from restaurant.models import Restaurant
from user.models import User


class ReviewSerializer(serializers.ModelSerializer):
    # unique_code 필드를 사용하여 restaurant를 참조
    restaurant = serializers.SlugRelatedField(
        slug_field="unique_code",  # unique_code를 참조하도록
        queryset=Restaurant.objects.all(),
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )  # 유저 필드 설정

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "restaurant",
            "score",
            "content",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]
