import environ
from pathlib import Path
import psycopg2
from psycopg2 import sql
import csv
import codecs


def load_initial_province_data():
    """province 정보를 담고 있는 csv 파일을 읽어 데이터 db에 저장하는 함수"""
    # .env 파일을 로드하여 환경 변수를 설정
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    env = environ.Env()
    env.read_env(f"{BASE_DIR}/.env")

    conn = None
    cur = None

    default_do_si = env("DEFAULT_DO_SI")

    try:
        # PostgreSQL 데이터베이스에 연결
        conn = psycopg2.connect(
            host=env("POSTGRESQL_HOST", default="postgres"),
            database=env("POSTGRES_DB", default="foodfinderdb"),
            user=env("POSTGRES_USER", default="postgres"),
            password=env("POSTGRES_PASSWORD", default="password"),
            port=env("POSTGRES_PORT"),
        )

        # 커서를 생성
        cur = conn.cursor()

        # CSV 파일 경로를 설정
        csv_file_path = (
            BASE_DIR / "src" / "sources" / env("SCV_FILE", default="sgg_lat_lon.csv")
        )

        # CSV 파일을 읽어 데이터베이스에 삽입
        # CSV 파일이 UTF-8 BOM으로 저장되어 있기에, 제거해서 파일 OPEN
        with codecs.open(csv_file_path, "rU", "utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                do_si = row["do-si"]
                city = row["sgg"]
                lon = float(row["lon"])
                lat = float(row["lat"])

                # 경기 지역 맛집만 정보 제공하므로 경기도 데이터만 추가
                if do_si == default_do_si:
                    insert_query = """
                    INSERT INTO province (city, lon, lat, created_at, updated_at)
                    VALUES (%s, %s, %s, NOW(), NOW())
                    """
                    try:
                        cur.execute(insert_query, (city, lat, lon))
                    except Exception as e:
                        conn.rollback()
                        print(f"An error occurred while inserting {city}: {e}")
                    else:
                        conn.commit()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # 커서와 연결이 존재하면 닫음
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    load_initial_province_data()
