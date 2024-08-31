from django.urls import path
from rest_framework.routers import DefaultRouter
from review.views import ReviewView

app_name = "restaurant"
router = DefaultRouter()

urlpatterns = []

urlpatterns += router.urls
