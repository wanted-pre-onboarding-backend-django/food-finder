from django.contrib import admin
from review.models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "restaurant",
        "score",
        "created_at",
    )
    list_filter = (
        "restaurant",
        "score",
        "created_at",
    )
    search_fields = (
        "user__account",
        "restaurant__name",
        "content",
    )
    readonly_fields = ("created_at",)


admin.site.register(Review, ReviewAdmin)
