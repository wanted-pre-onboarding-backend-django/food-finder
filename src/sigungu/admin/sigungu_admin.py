from django.contrib import admin
from province.models import Province


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    """Admin for Province model"""

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
