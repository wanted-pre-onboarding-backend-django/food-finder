from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "account",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "created_at",
            "updated_at",
            "is_lunch_rec_allowed",
            "latitude",
            "longitude",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "is_active": {"read_only": True},
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }
