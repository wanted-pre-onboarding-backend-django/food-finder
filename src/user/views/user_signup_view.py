from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError
from user.serializers import UserSignupSerializer
from user.models import User


class UserSignupAPIView(APIView):

    def post(self, request):
        account = request.data.get("account")
        email = request.data.get("email")
        password = request.data.get("password")
        if not password or not account or not email:
            raise ParseError
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()

            serializer = UserSignupSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
