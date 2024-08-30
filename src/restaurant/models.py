from django.db import models
from config.models import BaseModel


class Restaurant(BaseModel):
    """Restaurant Model Definition"""

    class BusinessStatus(models.TextChoices):
        # BSN_STATE_NM 영업상태명을 위한 초이스
        OPEN = ("영업", "영업")
        CLOSE = ("폐업", "폐업")

    class CategoryChoices(models.TextChoices):
        # CATEGORY 음식점 분류르 위한 초이스
        CHINESE = ("Genrestrtchifood", "중국식")
        JAPANESE = ("Genrestrtjpnfood", "일식")
        SOUP = ("Genrestrtsoup", "탕류(보신용)")
        PUB = ("Genrestrtstandpub", "정종/대포집/소주방")
        FAST_FOOD = ("Genrestrtchifood", "패스트푸드")

    SANITTN_BIZCOND_NM = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices,
        verbose_name="음식점 분류",
    )
    SIGUN_NM = models.CharField(
        max_length=255,
        verbose_name="시군명",
    )
    BIZPLC_NM = models.CharField(
        max_length=255,
        verbose_name="사업장명",
    )
    BSN_STATE_NM = models.CharField(
        max_length=2,
        choices=BusinessStatus.choices,
        verbose_name="영업상태명",
    )
    REFINE_ROADNM_ADDR = models.CharField(
        max_length=255,
        verbose_name="소재지도로명주소",
    )
    REFINE_LOTNO_ADDR = models.CharField(
        max_length=255,
        verbose_name="소재지지번주소",
    )
    REFINE_WGS84_LAT = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="WGS84위도",
    )
    REFINE_WGS84_LOGT = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="WGS84경도",
    )
    RATING = models.FloatField(
        default=0.0,
        verbose_name="평점",
    )

    class Meta:
        unique_together = (
            "BIZPLC_NM",
            "REFINE_LOTNO_ADDR",
        )  # 가게명과 주소의 조합이 유일하게 유지됨
        verbose_name = "맛집"
        verbose_name_plural = "맛집들"

    def __str__(self):
        return self.BIZPLC_NM
