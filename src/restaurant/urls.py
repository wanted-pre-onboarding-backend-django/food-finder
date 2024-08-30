from django.urls import path
from rest_framework.routers import DefaultRouter

from restaurant.views import (
    RestaurantListView,
    RestaurantDetailView,
)

app_name = "restaurant"
router = DefaultRouter()

urlpatterns = [
    path(
        "",
        RestaurantListView.as_view(),
        name="restaurant-list",
    ),
    path(
        "<int:pk>",
        RestaurantDetailView.as_view(),
        name="restaurant-detail",
    ),
]

urlpatterns += router.urls
