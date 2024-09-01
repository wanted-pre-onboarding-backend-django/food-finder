from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)

# Celery 설정
app = Celery(
    "config",
    broker="redis://localhost:6379/0",
)
app.conf.update(
    timezone="Asia/Seoul",  # 서울 기준으로 시간대 변경
    enable_utc=False,  # UTC 비활성화
)

# Django의 settings.py에서 정의된 모든 Celery 관련 설정을 가져오기
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)

# Django에서 자동으로 task를 검색하여 자동 로드
app.autodiscover_tasks(["config"])

app.conf.update(
    BROKER_URL="redis://localhost:6379",
    CELERY_TASK_SERIALIZER="json",
    CELERY_ACCEPT_CONTENT=["json"],
    CELERY_RESULT_SERIALIZER="json",
    CELERY_TIMEZONE="Asia/Seoul",
    CELERY_ENABLE_UTC=False,
    CELERY_BEAT_SCHEDULER="django_celery_beat.schedulers:DatabaseScheduler",
)

app.conf.beat_schedule = {
    "run-pipeline-every-monday-midnight": {
        "task": "config.tasks.run_full_pipeline",
        "schedule": crontab(
            minute=0,
            hour=0,
            day_of_week=1,
        ),
    },
}


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
