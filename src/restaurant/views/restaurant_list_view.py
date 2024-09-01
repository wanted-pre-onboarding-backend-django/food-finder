from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from restaurant.models import Restaurant
from restaurant.serializers import RestaurantListSerializer
from restaurant.utils.geo_distance import calculate_distance


class RestaurantListView(APIView):

    def get(self, request):
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")
        range_km = float(request.query_params.get("range", 1.0))  # 기본값: 1 km
        sort_by = request.query_params.get("sort", "distance")  # 기본 정렬: 거리순

        if not lat or not lon:
            return Response(
                {"error": "위도, 경도가 필요합니다"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 사용자 위치를 float로 변환
        user_location = (float(lat), float(lon))
        restaurants = Restaurant.objects.all()

        # 거리 계산하여 범위 내 식당 필터링
        filtered_restaurants = []
        for restaurant in restaurants:
            # 식당의 위도와 경도를 float으로 변환
            restaurant_location = (float(restaurant.lat), float(restaurant.lon))
            distance = calculate_distance(
                user_location[0],
                user_location[1],
                restaurant_location[0],
                restaurant_location[1],
            )
            if distance <= range_km:
                restaurant.distance = distance  # 거리 속성 추가
                filtered_restaurants.append(restaurant)

        # 정렬
        if sort_by == "rating":
            filtered_restaurants.sort(key=lambda x: x.rating, reverse=True)
        else:  # 거리순 정렬
            filtered_restaurants.sort(key=lambda x: x.distance)

        serializer = RestaurantListSerializer(filtered_restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
