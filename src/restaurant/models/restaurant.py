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
        CHINESE = ("중국식", "중국식")
        JAPANESE = ("일식", "일식")
        SOUP = ("탕류(보신용)", "탕류(보신용)")
        PUB = ("정종/대포집/소주방", "정종/대포집/소주방")
        FAST_FOOD = ("패스트푸드", "패스트푸드")

    unique_code = models.CharField(
        max_length=64,  # SHA-256 해시의 16진수 문자열 길이
        unique=True,  # 해시값이 유일해야 함
        verbose_name="SHA-256 Hash Value",
    )
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices,
        verbose_name="음식점 분류(위생업태명)",
    )
    province = models.ForeignKey(
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

        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"
        db_table = "restaurant"

    def __str__(self):
        return self.name
