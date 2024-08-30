from django.urls import path
from rest_framework.routers import DefaultRouter
from province.views import ProvinceListView


app_name = "province"
router = DefaultRouter()

urlpatterns = [
    path(
        "",
        ProvinceListView.as_view(),
        name="province-list",
    ),
]

urlpatterns += router.urls
