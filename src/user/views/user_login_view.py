from django.contrib.auth import authenticate
from rest_framework.response import Response

# from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt


class UserLogInAPIView(APIView):
    def post(self, request):
        account = request.data.get("account")
        password = request.data.get("password")
        if not account or not password:
            raise ParseError
        user = authenticate(
            account=account,
            password=password,
        )

        if user is not None:

            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )

            return Response({"token": token})
        else:
            raise AuthenticationFailed("아이디 또는 비밀번호가 잘못되었습니다.")
        