from typing import Any

from beartype import beartype
from celery import current_app
from celery.local import Proxy  # type: ignore
from celery.result import AsyncResult

from project.config import settings


@beartype
def create_celery() -> Proxy:
    _ = current_app.config_from_object(settings, namespace="CELERY")
    return current_app


@beartype
def get_task_info(task_id: str) -> dict[str, Any]:
    task = AsyncResult(task_id)
    response = {"state": task.state}
    if task.status == "FAILURE":
        return response | {"error": str(task.result)}
    else:
        return response
