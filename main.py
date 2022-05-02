from beartype import beartype
from watchgod import run_process

from project import create_app


app = create_app()
celery = app.celery_app  # type: ignore


if __name__ == "__main__":

    from subprocess import check_call  # noqa: S404

    @beartype
    def celery_worker() -> None:
        _ = run_process("./project", _run_worker)

    @beartype
    def _run_worker() -> None:
        _ = check_call(  # noqa: S603, S607
            ["celery", "-A", "main.celery", "worker", "--loglevel=info"]
        )

    celery_worker()
