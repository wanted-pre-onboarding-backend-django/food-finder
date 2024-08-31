from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from review.models import Review
from restaurant.models import Restaurant
from review.serializers import ReviewSerializer


class ReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, unique_code):
        # 특정 unique_code의 음식점 가져오기
        try:
            restaurant = Restaurant.objects.get(unique_code=unique_code)
        except Restaurant.DoesNotExist:
            return Response(
                {"error": "없는 음식점 입니다"}, status=status.HTTP_404_NOT_FOUND
            )

        # 요청에서 점수와 내용 가져오기
        data = {
            "user": request.user.id, 
            "restaurant": restaurant.unique_code,  # 문자열 PK unique_code 사용
            "score": request.data.get("score"),
            "content": request.data.get("content"),
        }

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
