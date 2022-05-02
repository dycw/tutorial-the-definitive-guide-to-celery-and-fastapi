from beartype import beartype
from celery import shared_task


@shared_task(name="project.users.tasks.divide")
@beartype
def divide(x: float, y: float) -> float:
    from time import sleep

    sleep(3)
    return x / y
