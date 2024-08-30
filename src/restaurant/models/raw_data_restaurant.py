from django.db import models
from config.models import BaseModel


class RdRestaurant(BaseModel):
    """ Raw data of Restaurant Model """

    sigun_nm = models.CharField(
        max_length=255,
    )
    sigun_cd = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    bizplc_nm = models.CharField(
        max_length=255,
    )
    licensg_de = models.CharField(
        max_length=100,
    )
    bsn_state_nm = models.CharField(
        max_length=50,
    )
    clsbiz_de = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    locplc_ar = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    grad_faclt_div_nm = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    male_enflpsn_cnt = models.IntegerField(
        null=True,
        blank=True,
        default=0,
    )
    yy = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    multi_use_bizestbl_yn = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    grad_div_nm = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    tot_faclt_scale = models.IntegerField(
        null=True,
        blank=True,
    )
    female_enflpsn_cnt = models.IntegerField(
        null=True,
        blank=True,
        default=0,
    )
    bsnsite_circumfr_div_nm = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    sanittn_indutype_nm = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    sanittn_bizcond_nm = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    tot_emply_cnt = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    refine_lotno_addr = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    refine_roadnm_addr = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    refine_zip_cd = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    refine_wgs84_logt = models.DecimalField(
        max_digits=15,
        decimal_places=10,
        null=True,
        blank=True,
    )
    refine_wgs84_lat = models.DecimalField(
        max_digits=15,
        decimal_places=10,
        null=True,
        blank=True,
    )

    class Meta:
        """ Meta definition for Raw Data of Restaurant """

        verbose_name = "RdRestaurant"
        verbose_name_plural = "RdRestaurant"
        db_table = "raw_data_restaurant"

        def __str__(self) -> str:
            return self.bizplc_nm
