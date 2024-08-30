from rest_framework import serializers
from score.models.score import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'restaurant', 'score', 'content']

    def validate_score(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("평점은 0점부터 5점 사이여야 합니다.")
        return value