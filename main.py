from beartype import beartype

from project import create_app


app = create_app()
celery = app.celery_app  # type: ignore


@beartype
def celery_worker() -> None:
    from subprocess import check_call  # noqa: S404

    from watchgod import run_process

    @beartype
    def run_worker() -> None:
        _ = check_call(  # noqa: S603, S607
            ["celery", "-A", "main.celery", "worker", "--loglevel=info"]
        )

    _ = run_process("./project", run_worker)


if __name__ == "__main__":
    celery_worker()
