"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from user.views import (
    UserSignupAPIView,
    UserLogInAPIView,
    UserLogOutAPIView,
)


schema_view = get_schema_view(
    openapi.Info(
        title="Food Finder API",
        default_version="v1",
        description="food-finder-backend",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="WantedPreOnboardingDjango@local.dev"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("users/", include("user.urls")),
    path("signup/", UserSignupAPIView.as_view()),
    path("login/", UserLogInAPIView.as_view()),
    path("logout/", UserLogOutAPIView.as_view()),
    path("provinces/", include("province.urls")),
    path("restaurants/", include("restaurant.urls")),
    path("score/", include("score.urls")),
]
