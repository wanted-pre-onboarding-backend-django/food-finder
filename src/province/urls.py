from django.urls import path
from rest_framework.routers import DefaultRouter

from province.views.province_list_view import (
ProvinceListView
)

app_name = "province"
router = DefaultRouter()

urlpatterns = [
    path(
        "",
        ProvinceListView.as_view(),
        name="Province-list",
    ),
]

urlpatterns += router.urls