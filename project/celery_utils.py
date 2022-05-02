from beartype import beartype
from celery import current_app
from celery.local import Proxy  # type: ignore

from project.config import settings


@beartype
def create_celery() -> Proxy:
    _ = current_app.config_from_object(settings, namespace="CELERY")
    return current_app
