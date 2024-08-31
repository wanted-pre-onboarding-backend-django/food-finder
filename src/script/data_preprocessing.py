import os
import sys
import json
import asyncio
import aiohttp
import django
import environ
import time
import hashlib
from pathlib import Path
from typing import List, Tuple
from decimal import Decimal
from tqdm.asyncio import tqdm_asyncio
from asgiref.sync import sync_to_async
from django.db import transaction


BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
env.read_env(f"{BASE_DIR}/.env")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


from restaurant.models import RdRestaurant, Restaurant
from province.models import Province


def hash_string(target_str):
    """
    param으로 넘겨 받은 string 해싱 처리(sha512)
    :param target_string: 해시로 바꿀 string
    :return: SHA-256 해시 문자열
    """

    # 해시 객체 생성
    sha256_hash = hashlib.sha256()

    # 입력 문자열 바이트로 인코딩해 해시 객체에 업데이트
    sha256_hash.update(target_str.encode("utf-8"))

    # 해시값 16진수 문자열로 변환
    return sha256_hash.hexdigest()


def convert_date(date_str):
    """
    Convert date string to 'YYYY-MM-DD' format
    :param date_str: 날짜 형태 format할 string
    :return: 0000-00-00 형태의 문자열
    """

    if "-" not in date_str and len(date_str) >= 8:
        return date_str[:4] + "-" + date_str[4:6] + "-" + date_str[6:]
    else:
        return date_str


async def preprocess_restaurant_data(
    session,
) -> Tuple[List[Restaurant], List[Restaurant]]:
    """
    맛집 raw data 전처리 전체 처리
    :param session: aiohttp.ClientSession
    :return: 새로 restaurant 테이블에 추가할 데이터와 기존 데이터 업데이트할 데이터
    """
    objects_to_update = []
    objects_to_create = []
    existing_restaurant_map = {}
    unique_codes_set = set()  # 중복 방지를 위한 set

    # 현재 존재하는 데이터 가져오기
    raw_datas = await sync_to_async(list)(RdRestaurant.objects.all())
    existing_restaurants = await sync_to_async(list)(Restaurant.objects.all())

    # unique_code 기준으로 값 가져오기
    existing_restaurant_map = {r.unique_code: r for r in existing_restaurants}

    # 비동기적으로 처리할 작업 리스트
    tasks = [
        process_raw_data(raw_data, existing_restaurant_map, session, unique_codes_set)
        for raw_data in raw_datas
    ]

    # tqdm_asyncio의 tqdm을 사용하여 진행 상황을 표시
    results = await tqdm_asyncio.gather(*tasks, desc="Data Preprocessing")

    # 결과를 합쳐서 objects_to_create, objects_to_update에 추가
    for result in results:
        objects_to_create.extend(result[0])
        objects_to_update.extend(result[1])

    return objects_to_create, objects_to_update


async def process_raw_data(
    raw_data, existing_restaurant_map, session, unique_codes_set
) -> Tuple[List[Restaurant], List[Restaurant]]:
    """
    맛집 raw data 전처리 (단일)
    :param session: aiohttp.ClientSession
    :return: 새로 restaurant 테이블에 추가할 데이터와 기존 데이터 업데이트할 데이터
    """

    objects_to_update = []
    objects_to_create = []

    # 도로명 주소, 지번주소, 위도, 경도 기본값 설정
    default_road_addr = "기본 도로 주소"
    default_lot_addr = "기본 지번 주소"
    default_lat = 0.0
    default_lon = 0.0

    # 네 컬럼 값 None일 시, default 값으로 대체
    road_addr = getattr(raw_data, "refine_roadnm_addr") or default_road_addr
    lot_addr = getattr(raw_data, "refine_lotno_addr") or default_lot_addr
    lat = getattr(raw_data, "refine_wgs84_lat") or default_lat
    lon = getattr(raw_data, "refine_wgs84_logt") or default_lon

    # 4 컬럼 값 중 하나라도 None일 시, 카카오 api 요청
    if (
        road_addr == default_road_addr
        and lot_addr == default_lot_addr
        and lat == default_lat
        and lon == default_lon
    ):
        # 지번주소 우선으로 요청, 지번주소 None일 시 도로명 주소 대신 요청
        request_addr = lot_addr or road_addr
        try:
            # 카카오 지도 api 데이터 요청한 뒤, 없는 컬럼 값만 해당 값으로 대체
            data = await fetch_address_info(session, request_addr)
            if data:
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
        except Exception as e:
            print(f"Error fetching address info: {e}")

    # 시도(province) 값 fk mapping
    # 없을 시 기본값 넣어줌
    try:
        province = await sync_to_async(Province.objects.get)(city=lot_addr.split()[1])
    except Province.DoesNotExist:
        province = await sync_to_async(Province.objects.first)()
        if not province:
            raise ValueError("No provinces data")

    # unique_code(pk) 제작
    # 음식점명 + 분야 + 영업 인허가일자 + 좌표 값으로 code 만든 뒤 hash 처리
    restaurant_name = getattr(raw_data, "bizplc_nm") or "누락"
    licensg_de = convert_date(getattr(raw_data, "licensg_de") or "0000-00-00")
    category = getattr(raw_data, "sanittn_bizcond_nm") or "정종/대포집/소주방"
    code_string = restaurant_name + category + licensg_de + str(lat) + str(lon)

    unique_code = hash_string(code_string)

    restaurant_data = {
        "unique_code": unique_code,
        "category": category,
        "province": province,
        "name": restaurant_name,
        "status": getattr(raw_data, "bsn_state_nm") or "폐업",
        "road_addr": road_addr,
        "lot_addr": lot_addr,
        "lat": Decimal(lat),
        "lon": Decimal(lon),
        "rating": Decimal(0.0),
    }

    # 해시값 기존 값과 일치하지 않을 시(중복값 아닐 시) 이하 로직 실행
    if unique_code not in unique_codes_set:
        unique_codes_set.add(unique_code)

        # 같은 해시값이 이미 존재할 경우, update
        if unique_code in existing_restaurant_map:
            restaurant_instance = existing_restaurant_map[unique_code]
            update_needed = False

            # 평점(rating) 제외한 나머지 값들 검증해서 변경해야 할 시에만 저장
            for attr, new_value in restaurant_data.items():
                if attr == "rating":
                    continue

                current_value = await sync_to_async(getattr)(restaurant_instance, attr)
                if current_value != new_value:
                    await sync_to_async(setattr)(restaurant_instance, attr, new_value)
                    update_needed = True

            if update_needed:
                objects_to_update.append(restaurant_instance)

        # 존재하지 않을 시 신규 데이터 저장
        # 이때 폐업 상태인 맛집 데이터는 아예 저장하지 않음
        else:
            if restaurant_data["status"] != "폐업":
                objects_to_create.append(Restaurant(**restaurant_data))

    return objects_to_create, objects_to_update


@sync_to_async
def save_restaurant_data(
    objects_to_create: List[Restaurant], objects_to_update: List[Restaurant]
):
    """
    bulk_create and bulk_update 사용해 데이터베이스에 반영
    :param objects_to_create: 새로 restaruant 테이블에 추가할 데이터
    :param objects_to_update: 기존 restaruant 데이터 업데이트
    """

    # 블록 내의 어떤 작업이라도 실패할 시, 트랜잭션 전체 롤백
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


async def fetch_address_info(session, addr):
    """
    kakao 주소 검색 api 호출해 주소에 해당하는 정보 반환 함수
    :param query: 검색할 주소 문자열
    :return: 검색된 주소 정보 또는 에러
    """

    KAKAO_API_URL = "https://dapi.kakao.com/v2/local/search/address.json"

    KAKAO_API_KEY = os.environ.get("KAKAO_API_KEY")

    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}

    params = {
        "query": addr,
    }

    # 서버에 api 요청
    async with session.get(KAKAO_API_URL, headers=headers, params=params) as response:
        if response.status == 200:
            text = await response.text()

            try:
                # text 형식으로 넘어온 data json 형식으로 변경
                data = json.loads(text)

                # 원하는 값 있을 시 return
                if len(data["documents"][0]) > 1 and "address" in data["documents"][0]:
                    return data["documents"][0]
                else:
                    print("Unexpected data structure or 'address' key is missing")
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
        else:
            print(f"Failed to fetch address datas: HTTP {response.status}")

    return None


async def data_preprocessing_pipline():
    """
    raw data 전처리 파이프라인 함수
    """
    async with aiohttp.ClientSession() as session:
        # 데이터 전처리 실행
        objects_to_create, objects_to_update = await preprocess_restaurant_data(session)

        # 신규 데이터 create or update 실행
        if objects_to_create or objects_to_update:
            await save_restaurant_data(objects_to_create, objects_to_update)

        await session.close()


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(data_preprocessing_pipline())
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Script executed in {elapsed_time:.2f} seconds")
