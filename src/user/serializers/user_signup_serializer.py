from rest_framework.serializers import ModelSerializer
from user.models import User

from django.contrib.auth import password_validation


class UserSignupSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "account",
            "email",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_password(self, value):
        # 비밀번호 검증
        password_validation.validate_password(value)
        return value
