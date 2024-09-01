# src/script/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from restaurant.utils.lunch_recommender import recommend_lunch  # 점심 추천 함수 임포트


def start():
    # APScheduler를 사용해 스케줄러를 시작
    scheduler = BackgroundScheduler(
        timezone=settings.TIME_ZONE
    )  # 백그라운드 스케줄러 생성
    scheduler.add_job(
        recommend_lunch, "cron", hour=11, minute=30
    )  # 매일 11:30에 실행되도록 설정
    scheduler.start()  # 스케줄러 시작
