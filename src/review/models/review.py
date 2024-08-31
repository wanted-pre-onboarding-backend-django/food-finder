from django.db import models
from user.models import User
from restaurant.models import Restaurant
from review.utils.update_restaurant_rating import update_restaurant_rating


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    restaurant = models.ForeignKey(
        Restaurant,
        related_name="reviews",
        on_delete=models.SET_NULL,
        null=True,
    )
    score = models.IntegerField(
        choices=[(i, i) for i in range(6)],
    )  # 0 ~ 5
    content = models.TextField(
        max_length=255,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 맛집 평점 업데이트
        update_restaurant_rating(self.restaurant)

    def __str__(self):
        return f"Review by {self.user} for {self.restaurant}"
