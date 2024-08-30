from django.db import models
from config.models import BaseModel


class Restaurant(BaseModel):
    """Restaurant Model Definition"""

    class BusinessStatus(models.TextChoices):
        # BSN_STATE_NM 영업상태명을 위한 초이스
        OPEN = ("영업", "영업")
        CLOSE = ("폐업", "폐업")

    class CategoryChoices(models.TextChoices):
        # CATEGORY 음식점 분류를 위한 초이스
        CHINESE = ("Genrestrtchifood", "중국식")
        JAPANESE = ("Genrestrtjpnfood", "일식")
        SOUP = ("Genrestrtsoup", "탕류(보신용)")
        PUB = ("Genrestrtstandpub", "정종/대포집/소주방")
        FAST_FOOD = ("Genrestrtchifood", "패스트푸드")

    category = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices,
        verbose_name="음식점 분류",
    )
    sigun = models.CharField(
        max_length=255,
        verbose_name="시군명",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="사업장명",
    )
    status = models.CharField(
        max_length=2,
        choices=BusinessStatus.choices,
        verbose_name="영업상태명",
    )
    road_addr = models.CharField(
        max_length=255,
        verbose_name="소재지도로명주소",
    )
    lot_addr = models.CharField(
        max_length=255,
        verbose_name="소재지지번주소",
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="WGS84위도",
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="WGS84경도",
    )
    rating = models.FloatField(
        default=0.0,
        verbose_name="평점",
    )

    class Meta:
        unique_together = (
            "name",
            "lot_addr",
        )  # 가게명과 주소의 조합이 유일하게 유지됨

    def __str__(self):
        return self.name
