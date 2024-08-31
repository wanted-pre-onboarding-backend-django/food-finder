from django.urls import path
from rest_framework.routers import DefaultRouter

from restaurant.views import (
    RestaurantListView,
    RestaurantDetailView,
)
from review.views import ReviewView

app_name = "restaurant"
router = DefaultRouter()

urlpatterns = [
    path(
        "",
        RestaurantListView.as_view(),
        name="restaurant-list",
    ),
    path(
        "<str:unique_code>/reviews/",
        ReviewView.as_view(),
        name="restaurant-review",
    ),
    path(
        "<str:unique_code>",
        RestaurantDetailView.as_view(),
        name="restaurant-detail",
    ),
]

urlpatterns += router.urls
