from beartype import beartype
from celery import shared_task


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
