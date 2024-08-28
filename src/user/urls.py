from django.urls import path
from rest_framework.routers import DefaultRouter

from user.views import (
    UserSignupAPIView,
    UserMeAPIView,
)

app_name = "user"
router = DefaultRouter()

urlpatterns = [
    path("", UserSignupAPIView.as_view()),
    path("me/", UserMeAPIView.as_view()),
]


urlpatterns += router.urls
