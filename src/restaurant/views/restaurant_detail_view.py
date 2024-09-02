from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from restaurant.models import Restaurant
from restaurant.serializers import RestaurantDetailSerializer
from review.models import Review
from review.serializers import ReviewSerializer
from django.core.cache import cache


class RestaurantDetailView(APIView):
    """맛집의 상세 보기"""

    def get(self, request, unique_code):
        # 캐시 키와 만료 시간 설정
        cache_key = f"restaurant_detail_{unique_code}"
        cache_timeout = 600  # 600초 (10분) 캐시 유효 기간

        # 캐시 확인
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            # 캐시 데이터 반환
            return Response(cached_data, status=status.HTTP_200_OK)

        # 캐시되지 않은 경우 DB 털기
        restaurant = get_object_or_404(Restaurant, unique_code=unique_code)

        # 해당 맛집에 대한 리뷰 리스트 조회
        reviews = Review.objects.filter(restaurant=restaurant).order_by(
            "-created_at"
        )  # created_at 내림차순 정렬

        restaurant_serializer = RestaurantDetailSerializer(restaurant)
        review_serializer = ReviewSerializer(reviews, many=True)
        serialized_data = {
            "restaurant": restaurant_serializer.data,
            "reviews": review_serializer.data,
        }

        # 캐시에 저장
        cache.set(cache_key, serialized_data, cache_timeout)

        # 맛집 상세 정보와 리뷰 리스트를 함께 반환
        return Response(
            serialized_data,
            status=status.HTTP_200_OK,
        )
