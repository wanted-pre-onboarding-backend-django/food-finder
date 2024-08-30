from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from province.models import Province
from province.serializers import ProvinceSerializer


class ProvinceListView(APIView):
    def get(self, request):
        # 시군구 목록
        provinces = Province.objects.all()
        serializer = ProvinceSerializer(provinces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
