from django.urls import path
from score.views.score_views import ReviewViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', ReviewViewSet, basename='review')  # 빈 URL 패턴으로 연결

urlpatterns = router.urls