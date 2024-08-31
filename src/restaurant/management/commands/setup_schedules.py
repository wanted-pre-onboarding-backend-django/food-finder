from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json


class Command(BaseCommand):
    help = "Set up Celery Beat schedules"

    def handle(self, *args, **kwargs):
        # 데이터 수집 작업 스케줄 설정
        # 매주 월요일 자정에 스케쥴러 실행
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute="0",  # 0분
            hour="0",  # 오전 12시
            day_of_week="1",  # 월요일
            day_of_month="*",
            month_of_year="*",
        )

        data_collection_task, created = PeriodicTask.objects.update_or_create(
            name="Data Collection Task",
            defaults={
                "crontab": schedule,
                "task": "restaurant.tasks.data_collection_task",  # tasks.py에 세팅해둔 작업명
            },
        )

        # 데이터 전처리 작업 스케줄 설정
        data_pipeline_task, created = PeriodicTask.objects.update_or_create(
            name="Data Preprocessing Task",
            defaults={
                "crontab": schedule,
                "task": "restaurant.tasks.data_preprocessing_task",  # tasks.py에 세팅해둔 작업명
            },
        )

        self.stdout.write(self.style.SUCCESS("Successfully set up schedules"))
