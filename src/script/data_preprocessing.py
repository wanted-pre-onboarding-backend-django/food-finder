import os
import sys
import math
import json
import asyncio
import aiohttp
import requests
import django
import environ
import time
from datetime import datetime
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple
from decimal import Decimal
from tqdm.asyncio import tqdm_asyncio
from asgiref.sync import sync_to_async
from django.db import transaction

from restaurant.models import Restaurant, RdRestaurant
from province.models import Province


def hash_string(target_string):
    """
    param으로 넘겨 받은 string 해싱 처리(sha256)
    :param target_string: 해시로 바꿀 string
    """

    # 해시 객체 생성
    sha256_hash = hashlib.sha256()

    # 입력 문자열 바이트로 인코딩해 해시 객체에 업데이트
    sha256_hash.update(target_string.encode("utf-8"))

    # 해시값 16진수 문자열로 변환
    return sha256_hash.hexdigest()


def preprocess_restaurant_data() -> Tuple[List[Restaurant], List[Restaurant]]:
    """
    맛집 raw data 전처리
    :param objects_to_create: 새로 restaruant 테이블에 추가할 데이터
    :param objects_to_update: 기존 restaruant 데이터 업데이트할 데이터
    """
    objects_to_update = []
    objects_to_create = []
    existing_restaurant_map = {}

    # TODO : 현재 존재하는 맛집 PK만 모아둔 테이블 만들어서 최적화하기
    raw_datas = RdRestaurant.objects.all()
    existing_restaurants = Restaurant.objects.all()

    # unique_code 기준으로 값 가져오기
    existing_restaurant_map = {r.unique_code: r for r in existing_restaurants}

    for raw_data in raw_datas:

        # 기본값 설정
        default_road_addr = "기본 도로 주소"
        default_lot_addr = "기본 지번 주소"
        default_lat = 0.0
        default_lon = 0.0

        # 도로명 주소, 지번주소
        road_addr = raw_data.get("refine_roadnm_addr", default_road_addr)
        lot_addr = raw_data.get("refine_lotno_addr", default_lot_addr)

        # 위도, 경도
        lat = raw_data.get("refine_wgs84_lat", default_lat)
        lon = raw_data.get("refine_wgs84_logt", default_lon)

        # 네 데이터 중 하나라도 null이면, kakao api 요청
        if (
            road_addr == default_road_addr
            and lot_addr == default_lot_addr
            and lat == default_lat
            and lon == default_lon
        ):
            request_addr = lot_addr or road_addr

            data = get_address_info(request_addr)

            # 데이터 정확하게 불러왔다면, 수정
            if data is not None:
                # 본래 null이 아니었던 경우에는 값을 업데이트하지 않음
                if road_addr == default_road_addr:
                    road_addr = data.get("road_address", {}).get(
                        "address_name", road_addr
                    )
                if lot_addr == default_lot_addr:
                    lot_addr = data.get("address", {}).get("address_name", lot_addr)
                if lat == default_lat:
                    lat = data.get("x", lat)
                if lon == default_lon:
                    lon = data.get("y", lon)

        # province 가져오기
        try:
            province = Province.objects.get(city=lot_addr.split()[1])
        except Province.DoesNotExist:
            # 없을 시 기본값 세팅
            province = Province.objects.first()
            if not province:
                raise ValueError("No provinces data")

        # unique 코드 제작 (음식점명 + 인허가일자 + 위치정보)
        restaurant_name = raw_data.get("bizplc_nm", "사업장명")
        licensg_de = convert_date(raw_data.get("licensg_de", "0000-00-00"))
        unique_code = hash_string(restaurant_name + licensg_de + lat + lon)

        restaurant_data = {
            "unique_code": unique_code,
            "category": raw_data.get("category", "정종/대포집/소주방"),
            "province": province,
            "name": restaurant_name,
            "status": raw_data.get("sanittn_bizcond_nm", "영업"),
            "road_addr": road_addr,
            "lot_addr": lot_addr,
            "lat": Decimal(lat),
            "lon": Decimal(lon),
            "rating": Decimal(raw_data.get("rating", 0.0)),
        }

        # 이미 존재하는 값일 시 값 업데이트 해서 objects_to_update에 추가
        if unique_code in existing_restaurant_map:
            restaurant_instance = existing_restaurant_map[unique_code]
            update_needed = False

            # rating 제외하고 변경사항 있을 시, 수정
            for attr, new_value in restaurant_data.items():
                if attr == "rating":
                    continue

                current_value = getattr(restaurant_instance, attr)
                if current_value != new_value:
                    setattr(restaurant_instance, attr, new_value)
                    update_needed = True

            if update_needed:
                objects_to_update.append(restaurant_instance)

        # 존재하지 않을 시 새로 instance 만들어서 objects_to_create에 추가
        else:
            objects_to_create.append(Restaurant(**restaurant_data))

    return objects_to_create, objects_to_update


def save_restaurant_data(
    objects_to_create: List[Restaurant], objects_to_update: List[Restaurant]
):
    """
    bulk_create and bulk_update 사용해 데이터베이스에 반영
    :param objects_to_create: 새로 restaruant 테이블에 추가할 데이터
    :param objects_to_update: 기존 restaruant 데이터 업데이트
    """

    with transaction.atomic():
        if objects_to_create:
            Restaurant.objects.bulk_create(objects_to_create)

        if objects_to_update:
            Restaurant.objects.bulk_update(
                objects_to_update,
                fields=[
                    "category",
                    "province",
                    "name",
                    "status",
                    "road_addr",
                    "lot_addr",
                    "lat",
                    "lon",
                ],
            )


def get_address_info(addr):
    """
    kakao 주소 검색 api 호출해 주소에 해당하는 정보 반환 함수
    :param query: 검색할 주소 문자열
    :return: 검색된 주소 정보 또는 에러
    """

    KAKAO_API_URL = "https://dapi.kakao.com/v2/local/search/address.json"

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    env = environ.Env()
    env.read_env(f"{BASE_DIR}/.env")

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()

    KAKAO_API_KEY = os.environ.get("KAKAO_API_KEY")

    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}

    params = {
        "query": addr,
    }

    try:
        # api 요청
        response = requests.get(
            KAKAO_API_URL,
            headers=headers,
            params=params,
        )

        # 오류 발생 시 오류 raise
        response.raise_for_status()
        data = response.json()

        return data["documents"][0]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def convert_date(date_str):
    """Convert date string to 'YYYY-MM-DD' format"""

    if "-" in date_str:
        return date_str

    return date_str[:4] + "-" + date_str[4:6] + "-" + date_str[6:]
