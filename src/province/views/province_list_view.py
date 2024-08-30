from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from province.serializers.province_serializers import ProvinceSerializer


# 시군구 목록보기
class ProvinceListView(APIView):

    def get(self, request):

        # 응답 반환
        return Response(ProvinceSerializer, status=status.HTTP_200_OK)

