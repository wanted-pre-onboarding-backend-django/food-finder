from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user.models import User
import jwt


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Cookie에서 JWT 토큰 추출 ---> 요구사항과 같이 헤더에서 추출로 변경
        # token = request.COOKIES.get("jwt")
        token = request.headers.get("jwt")

        if not token:
            return None
        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        pk = decoded.get("pk")
        if not pk:
            raise AuthenticationFailed("유효하지 않은 jwt토큰입니다")
        try:
            user = User.objects.get(pk=pk)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("존재하지않는 유저입니다")
        