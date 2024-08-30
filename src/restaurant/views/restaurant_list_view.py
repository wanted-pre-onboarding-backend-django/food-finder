from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from restaurant.models import Restaurant
from restaurant.serializers import RestaurantListSerializer
import math


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # 지구의 반지름 (km)

    # 위도와 경도를 라디안으로 변환
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Haversine 공식
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # 두 지점 사이의 거리 계산
    distance = R * c

    return distance


class RestaurantListView(APIView):

    def get(self, request):
        # 쿼리 파라미터 가져오기
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")
        range_km = float(request.query_params.get("range", 1.0))  # 기본값: 1 km
        sort_by = request.query_params.get("sort", "distance")  # 기본 정렬: 거리순

        # 필수 값 검증
        if not lat or not lon:
            return Response(
                {"error": "위도, 경도가 필요합니다"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 사용자 위치를 float로 변환
        user_location = (float(lat), float(lon))
        restaurants = Restaurant.objects.all()

        # 거리 계산하여 범위 내의 맛집 필터링
        filtered_restaurants = []
        for restaurant in restaurants:
            # Restaurant 모델의 lat, lon을 float으로 변환
            restaurant_location = (float(restaurant.lat), float(restaurant.lon))
            distance = calculate_distance(
                user_location[0],
                user_location[1],
                restaurant_location[0],
                restaurant_location[1],
            )
            if distance <= range_km:
                restaurant.distance = distance  # 동적으로 거리 추가
                filtered_restaurants.append(restaurant)

        # 정렬 옵션에 따른 정렬
        if sort_by == "rating":
            filtered_restaurants.sort(key=lambda x: x.rating, reverse=True)
        else:  # 거리순 정렬
            filtered_restaurants.sort(key=lambda x: x.distance)

        # 데이터 직렬화 및 반환
        serializer = RestaurantListSerializer(filtered_restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
