from celery import shared_task
import asyncio

from script.data_collection import data_collection_pipeline
from script.data_preprocessing import data_preprocessing_pipline


@shared_task
def run_full_pipeline():
    # data 수집, data 전처리 작업 순차 실행
    asyncio.run(data_collection_pipeline())
    asyncio.run(data_preprocessing_pipline())
