from logging import getLogger
from random import choice
from sys import stdout

from beartype import beartype
from celery.result import AsyncResult
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from requests import post

from project.users import users_router
from project.users.schemas import UserBody
from project.users.tasks import sample_task
from project.users.tasks import task_process_notification


logger = getLogger(__name__)
templates = Jinja2Templates(directory="project/users/templates")


@beartype
def api_call(_email: str) -> None:
    # used for testing a failed api call
    if choice([True, False]):  # noqa: S311
        raise Exception("random processing error")

    # used for simulating a call to a third-party api
    _ = post("https://httpbin.org/delay/5")


@users_router.get("/form/")
@beartype
def form_example_get(request: Request) -> Response:
    return templates.TemplateResponse("form.html", {"request": request})


@users_router.post("/form/")
@beartype
def form_example_post(user_body: UserBody) -> JSONResponse:
    task = sample_task.delay(user_body.email)
    return JSONResponse({"task_id": task.task_id})


@users_router.get("/task_status/")
@beartype
def task_status(task_id: str) -> JSONResponse:
    if (task := AsyncResult(task_id)).state == "FAILURE":
        error = str(task.result)
        response = {"state": task.state, "error": error}
    else:
        response = {"state": task.state}
    return JSONResponse(response)


@users_router.post("/webhook_test/")
def webhook_test() -> str:
    if choice([True, False]):  # noqa: S311
        # mimic an error
        raise Exception()

    # blocking process
    _ = post("https://httpbin.org/delay/5")
    return "pong"


@users_router.post("/webhook_test_2/")
def webhook_test_2() -> str:
    task = task_process_notification.delay()
    _ = stdout.write(f"{task.id}\n")
    return "pong"


@users_router.get("/form_ws/")
def form_ws_example(request: Request) -> Response:
    return templates.TemplateResponse("form_ws.html", {"request": request})


@users_router.get("/form_socketio/")
def form_socketio_example(request: Request) -> Response:
    return templates.TemplateResponse(
        "form_socketio.html", {"request": request}
    )
