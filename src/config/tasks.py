import time
import asyncio
from celery import shared_task
from script.data_collection import data_collection_pipeline
from script.data_preprocessing import data_preprocessing_pipeline


@shared_task
def data_collection_task():
    """데이터 수집 task"""
    start_time = time.time()
    asyncio.run(data_collection_pipeline())
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Data collection executed in {elapsed_time:.2f} seconds")


@shared_task
def data_preprocessing_task():
    """데이터 전처리 task"""
    start_time = time.time()
    asyncio.run(data_preprocessing_pipeline())
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Data preprocessing executed in {elapsed_time:.2f} seconds")
