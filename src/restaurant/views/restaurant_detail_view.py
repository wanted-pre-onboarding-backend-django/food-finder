from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from restaurant.models import Restaurant
from restaurant.serializers import RestaurantDetailSerializer
from reviews.models import Review  # 리뷰 모델을 사용한다고 가정
from reviews.serializers import ReviewSerializer  # 리뷰 시리얼라이저를 사용한다고 가정


class RestaurantDetailView(APIView):
    """
    특정 맛집의 상세 정보를 조회하는 API View.
    """

    def get(self, request, restaurant_id):
        # 맛집 객체를 가져오거나 404 반환
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        # 해당 맛집에 대한 리뷰 리스트 조회
        reviews = Review.objects.filter(restaurant=restaurant).order_by(
            "-created_at"
        )  # created_at을 기준으로 내림차순 정렬

        # 맛집 상세 정보 직렬화
        restaurant_serializer = RestaurantDetailSerializer(restaurant)

        # 리뷰 리스트 직렬화
        review_serializer = ReviewSerializer(reviews, many=True)

        # 맛집 상세 정보와 리뷰 리스트를 함께 반환
        return Response(
            {
                "restaurant": restaurant_serializer.data,
                "reviews": review_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
