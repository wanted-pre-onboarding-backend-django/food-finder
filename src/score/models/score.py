from django.db import models
from restaurant.models import Restaurant
from user.models import User 

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name='reviews', on_delete=models.CASCADE)
    score = models.IntegerField()
    content = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_restaurant_rating()

    def update_restaurant_rating(self):
        reviews = self.restaurant.reviews.all()
        average_rating = reviews.aggregate(models.Avg('score'))['score__avg']
        self.restaurant.rating = average_rating
        self.restaurant.save()