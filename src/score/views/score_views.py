from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from score.models.score import Review
from score.serializers.score_serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)