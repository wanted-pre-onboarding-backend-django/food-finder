from django.apps import AppConfig


class ConfigConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "config"

    def ready(self):
        # 스케줄러를 시작하는 코드
        from script.lunch_rec_scheduler import (
            start,
        )  # scheduler.py에서 start 함수 임포트

        start()  # 스케줄러 시작
