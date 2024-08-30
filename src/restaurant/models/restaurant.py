from django.db import models
from config.models import BaseModel
from province.models import Province


class Restaurant(BaseModel):
    """Restaurant Model Definition"""

    class BusinessStatus(models.TextChoices):
        # BSN_STATE_NM 영업상태명을 위한 초이스
        OPEN = ("영업", "영업")
        CLOSE = ("폐업", "폐업")

    class CategoryChoices(models.TextChoices):
        # CATEGORY 음식점 분류를 위한 초이스
        CHINESE = ("Genrestrtfastfood", "중국식")
        JAPANESE = ("Genrestrtjpnfood", "일식")
        SOUP = ("Genrestrtsoup", "탕류(보신용)")
        PUB = ("Genrestrtstandpub", "정종/대포집/소주방")
        FAST_FOOD = ("Genrestrtchifood", "패스트푸드")

    category = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices,
        verbose_name="음식점 분류(위생업태명)",
    )
    sigun = models.ForeignKey(
        Province,
        on_delete=models.DO_NOTHING,
        verbose_name="시군구",
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
    rating = models.DecimalField(
        max_digits=3,  # 점까지 포함한 스트링으로 저장
        decimal_places=1,  # 소수점 이하 한 자리를 의미
        default=0.0,
        verbose_name="평점",
    )

    class Meta:
        """Meta definition for Restaurant."""

        unique_together = (
            "name",
            "lot_addr",
        )  # 가게명과 주소의 조합이 유일하게 유지됨
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"
        db_table = "restaurant"

    def __str__(self):
        return self.name
