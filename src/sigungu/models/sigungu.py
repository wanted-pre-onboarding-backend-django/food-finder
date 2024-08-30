from django.db import models
from config.models import BaseModel


class Province(BaseModel):

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

    def __str__(self):
        return self.city
