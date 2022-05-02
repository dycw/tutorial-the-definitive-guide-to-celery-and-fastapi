from fastapi import APIRouter


users_router = APIRouter(prefix="/users")


from project.users import models  # type: ignore # isort:skip # noqa
from project.users import tasks  # type: ignore # isort:skip # noqa
from project.users import views  # type: ignore # isort:skip # noqa
