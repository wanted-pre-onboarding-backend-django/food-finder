import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("config")
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)
app.autodiscover_tasks()
app.conf.timezone = "Asia/Seoul"

app.conf.beat_schedule = {
    # data_pipline 작업 매주 월요일 0시 0분에 실행
    "test-schedule": {
        "task": "config.tasks.run_full_pipeline",
        "schedule": crontab(
            minute=0,
            hour=0,
            day_of_week="monday",
        ),
    }
}
