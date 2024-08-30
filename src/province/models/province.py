from django.db import models
from config.models import BaseModel


class Province(BaseModel):
    """Raw data of Province Model"""

    city = models.CharField(
        max_length=50,
        verbose_name="시 명칭",
    )
    lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="위도",
    )
    lon = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="경도",
    )

    class Meta:
        """Meta definition for Province"""

        verbose_name = "Province"
        verbose_name_plural = "Provinces"
        db_table = "province"

        def __str__(self) -> str:
            return self.city
