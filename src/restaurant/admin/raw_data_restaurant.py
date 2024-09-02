import csv
from django.http import HttpResponse
from django.contrib import admin
from restaurant.models import RdRestaurant


@admin.register(RdRestaurant)
class RdRestaurantAdmin(admin.ModelAdmin):
    """Admin View for RdRestrtAdmin"""

    list_display = (
        "sigun_nm",
        "sigun_cd",
        "bizplc_nm",
        "licensg_de",
        "bsn_state_nm",
        "clsbiz_de",
        "locplc_ar",
        "grad_faclt_div_nm",
        "male_enflpsn_cnt",
        "yy",
        "multi_use_bizestbl_yn",
        "grad_div_nm",
        "tot_faclt_scale",
        "female_enflpsn_cnt",
        "bsnsite_circumfr_div_nm",
        "sanittn_indutype_nm",
        "sanittn_bizcond_nm",
        "tot_emply_cnt",
        "refine_lotno_addr",
        "refine_roadnm_addr",
        "refine_zip_cd",
        "refine_wgs84_logt",
        "refine_wgs84_lat",
    )

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={meta}.csv"
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected as CSV"
