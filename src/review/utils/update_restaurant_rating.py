from django.db.models import Avg
from restaurant.models import Restaurant


def update_restaurant_rating(restaurant: Restaurant):
    # 주어진 Restaurant의 모든 리뷰 평점을 계산
    # 지연 임포트 -> 순환 참조 문제 해결
    from review.models import Review

    if restaurant is None:
        return 

    reviews = Review.objects.filter(restaurant=restaurant)
    if reviews.exists():
        average_rating = reviews.aggregate(Avg("score"))["score__avg"]
        restaurant.rating = average_rating
    else:
        restaurant.rating = 0.0
    restaurant.save()
