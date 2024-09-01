from restaurant.models import Restaurant
from user.models import User
from .geo_distance import calculate_distance
from .discord_webhook import send_discord_webhook


def sort_by_rating(restaurant):
    # 음식점을 평점순으로 정렬하기 위한 키 함수.
    return restaurant.rating


def recommend_lunch():
    """
    점심 추천 서비스를 사용하는 유저를 대상으로 주변 맛집을 추천하는 함수.
    """
    users = User.objects.filter(
        is_lunch_rec_allowed=True
    )  # 점심 추천 서비스가 허용된 유저 필터링

    for user in users:
        # 사용자의 위도와 경도
        user_lat, user_lon = user.latitude, user.longitude

        # 500 미터 이내의 맛집 필터링
        nearby_restaurants = Restaurant.objects.filter(status="영업").all()
        nearby_restaurants = [
            restaurant
            for restaurant in nearby_restaurants
            if calculate_distance(
                user_lat, user_lon, float(restaurant.lat), float(restaurant.lon)
            )
            <= 0.5
        ]

        # 카테고리별로 맛집 평점순 정렬 후 상위 5개씩 선택
        category_restaurants = {}
        for restaurant in nearby_restaurants:
            category = restaurant.category
            if category not in category_restaurants:
                category_restaurants[category] = []

            # 카테고리에 음식점 추가
            category_restaurants[category].append(restaurant)

            # 평점순으로 정렬하여 상위 5개 유지
            sorted_restaurants = sorted(
                category_restaurants[category],
                key=sort_by_rating,  # 평점을 기준으로 정렬
                reverse=True,  # 내림차순 정렬
            )
            category_restaurants[category] = sorted_restaurants[:5]  # 상위 5개 선택

        # Discord Webhook을 통해 메시지 보내기
        send_discord_webhook(user, category_restaurants)
