from django.contrib import admin
from sigungu.models import Sigungu


@admin.register(Sigungu)
class SigunguAdmin(admin.ModelAdmin):
    """Admin for Sigungu model"""

    list_display = (
        "city",
        "lat",
        "lon",
    )
    search_fields = ("city",)

    ordering = ("city",)

    fieldsets = (
        (None, {"fields": ("city",)}),
        ("Location Information", {"fields": ("lat", "lon")}),
    )
