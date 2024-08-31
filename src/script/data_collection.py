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
from pathlib import Path
from tqdm.asyncio import tqdm_asyncio
from asgiref.sync import sync_to_async


BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
env.read_env(f"{BASE_DIR}/.env")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


from restaurant.models import RdRestaurant


API_KEY = os.environ.get("API_KEY")
BASE_URL = "https://openapi.gg.go.kr"
DATA_TYPES = [
    "Genrestrtfastfood",
    "Genrestrtjpnfood",
    "Genrestrtchifood",
    "Genrestrtsoup",
    "Genrestrtstandpub"
]


async def fetch_total_count(session, data_type):
    url = f"{BASE_URL}/{data_type}?key={API_KEY}&Type=json&pIndex=1&pSize=1"
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류가 발생했는지 확인
        data = response.json()
        return data[data_type][0]['head'][0]['list_total_count']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


async def fetch_data(session, data_type, page):
    url = f"{BASE_URL}/{data_type}?key={API_KEY}&Type=json&pIndex={page}&pSize=1000"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }

    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            text = await response.text()

            try:
                data = json.loads(text)

                if data_type in data:
                    if len(data[data_type]) > 1 and 'row' in data[data_type][1]:
                        return data[data_type][1]['row']
                    else:
                        print("Unexpected data structure or 'row' key missing.")
                else:
                    print(f"{data_type} not found in response.")
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
        else:
            print(f"Failed to fetch data: HTTP {response.status}")

    return None


@sync_to_async
def save_data_to_db(objects_to_create):
    RdRestaurant.objects.bulk_create(objects_to_create)


async def save_to_db(data_list):
    objects_to_create = [
        RdRestaurant(
            sigun_nm=item.get("SIGUN_NM"),
            sigun_cd=item.get("SIGUN_CD"),
            bizplc_nm=item.get("BIZPLC_NM"),
            licensg_de=item.get("LICENSG_DE"),
            bsn_state_nm=item.get("BSN_STATE_NM"),
            clsbiz_de=item.get("CLSBIZ_DE"),
            locplc_ar=item.get("LOCPLC_AR"),
            grad_faclt_div_nm=item.get("GRAD_FACLT_DIV_NM"),
            male_enflpsn_cnt=item.get("MALE_ENFLPSN_CNT"),
            yy=item.get("YY"),
            multi_use_bizestbl_yn=item.get("MULTI_USE_BIZESTBL_YN"),
            grad_div_nm=item.get("GRAD_DIV_NM"),
            tot_faclt_scale=item.get("TOT_FACLT_SCALE"),
            female_enflpsn_cnt=item.get("FEMALE_ENFLPSN_CNT"),
            bsnsite_circumfr_div_nm=item.get("BSNSITE_CIRCUMFR_DIV_NM"),
            sanittn_indutype_nm=item.get("SANITTN_INDUTYPE_NM"),
            sanittn_bizcond_nm=item.get("SANITTN_BIZCOND_NM"),
            tot_emply_cnt=item.get("TOT_EMPLY_CNT"),
            refine_lotno_addr=item.get("REFINE_LOTNO_ADDR"),
            refine_roadnm_addr=item.get("REFINE_ROADNM_ADDR"),
            refine_zip_cd=item.get("REFINE_ZIP_CD"),
            refine_wgs84_logt=item.get("REFINE_WGS84_LOGT"),
            refine_wgs84_lat=item.get("REFINE_WGS84_LAT")
        )
        for item in data_list
    ]
    await save_data_to_db(objects_to_create)


async def data_collection_pipeline():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for data_type in DATA_TYPES:
            total_count = await fetch_total_count(session, data_type)
            total_pages = math.ceil(total_count / 1000)

            for page in range(1, total_pages + 1):
                tasks.append(fetch_data(session, data_type, page))

        for task in tqdm_asyncio(asyncio.as_completed(tasks), total=len(tasks), desc="Collecting data"):
            data_list = await task
            if data_list:
                await save_to_db(data_list)


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(data_collection_pipeline())
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Script executed in {elapsed_time:.2f} seconds")
