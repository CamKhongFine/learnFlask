from celery import shared_task
from app_config.config import create_app
from time import sleep

flask_app = create_app()
celery_app = flask_app.extensions["celery"]

@shared_task(ignore_result=False)
def long_running_task(iterations) -> int:
    result = 0
    for i in range(iterations):
        result += i
        sleep(10)
    return result

@shared_task(ignore_result=False)
def short_running_task(iterations) -> int:
    result = 0
    for i in range(iterations):
        result += i
    return result

@shared_task(ignore_result=False)
def chord_running_task(list):
    print("chord_task")
    return 6

@shared_task(ignore_result=False)
def chain_running_task(list):
    print("chain_task")
    return 6

@shared_task(autoretry_for = (Exception,), retry_kwargs={"max_retries" : 5, "countdown" : 5})     # Su dung countdown thay vi
def retry_running_task(iteration):
    for i in range(iteration):
        print("Oke")
    print("retry_task")
    return 1

@shared_task()
def chunk_running_task(a, b):
    return a + b
