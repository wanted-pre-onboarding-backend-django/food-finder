from rest_framework.response import Response
from rest_framework.views import APIView
from province.models import Province
from province.serializers import ProvinceSerializer
from django.core.cache import cache
from rest_framework import status


class ProvinceListView(APIView):
    def get(self, request):
        # 시군구 목록
        cache_key = "province_list"  # 캐시 키 설정
        cache_timeout = 60 * 60 * 6  # 캐시 만료 시간 (6시간)

        # 캐시에서 데이터 가져오기
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            # 캐시된 데이터가 있는 경우
            return Response(cached_data, status=status.HTTP_200_OK)

        # 캐시된 데이터가 없는 경우 DB털기
        provinces = Province.objects.all()
        serializer = ProvinceSerializer(provinces, many=True)
        serialized_data = serializer.data

        # 캐시에 데이터 저장
        cache.set(cache_key, serialized_data, cache_timeout)

        return Response(serializer.data, status=status.HTTP_200_OK)
