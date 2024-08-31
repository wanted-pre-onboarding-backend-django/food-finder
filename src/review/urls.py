from django.urls import path
from rest_framework.routers import DefaultRouter
from review.views import ReviewView

app_name = "restaurant"
router = DefaultRouter()

urlpatterns = [
    path(
        "/restaurants/<int:restaurant_id>/reviews/",
        ReviewView.as_view(),
        name="create_review",
    ),
]

urlpatterns += router.urls
