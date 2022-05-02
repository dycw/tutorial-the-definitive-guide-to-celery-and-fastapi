from random import choice
from typing import Any

from beartype import beartype
from celery import shared_task
from celery.utils.log import get_task_logger
from requests import post


logger = get_task_logger(__name__)


@shared_task(name="project.users.tasks.divide")
@beartype
def divide(x: float, y: float) -> float:
    # from celery.contrib.rdb import set_trace # noqa: E800
    # set_trace() # noqa: E800

    from time import sleep

    sleep(3)
    return x / y


@shared_task(name="project.users.tasks.sample_task")
@beartype
def sample_task(email: str) -> None:
    from project.users.views import api_call

    api_call(email)


@shared_task(name="project.users.tasks.task_process_notification", bind=True)
@beartype
def task_process_notification(self: Any) -> None:
    try:
        if choice([True, False]):  # noqa: S311
            # mimic random error
            raise Exception()

        # blocking process
        _ = post("https://httpbin.org/delay/5")
    except Exception as e:
        logger.error("exception raises, it will be retried after 5 seconds")
        raise self.retry(exc=e, countdown=5)
