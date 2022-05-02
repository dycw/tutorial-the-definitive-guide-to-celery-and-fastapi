from project import create_app  # noqa: INP001


app = create_app()
celery = app.celery_app  # type: ignore
