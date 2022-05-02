from beartype import beartype
from celery import current_app
from celery.local import Proxy

from project.config import settings


@beartype
def create_celery() -> Proxy:
    current_app.config_from_object(settings, namespace="CELERY")
    return current_app
