from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from restaurant.models import Restaurant
from restaurant.serializers import RestaurantDetailSerializer
from review.models import Review  
from review.serializers import ReviewSerializer 


class RestaurantDetailView(APIView):
    """맛집의 상세 보기"""

    def get(self, request, unique_code):
        restaurant = get_object_or_404(Restaurant, unique_code=unique_code)

        #해당 맛집에 대한 리뷰 리스트 조회
        reviews = Review.objects.filter(restaurant=restaurant).order_by(
            "-created_at"
        )  # created_at 내림차순 정렬

        restaurant_serializer = RestaurantDetailSerializer(restaurant)
        review_serializer = ReviewSerializer(reviews, many=True)

        #맛집 상세 정보와 리뷰 리스트를 함께 반환
        return Response(
            {
                "restaurant": restaurant_serializer.data,
                "reviews": review_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
