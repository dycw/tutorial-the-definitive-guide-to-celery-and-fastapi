from fastapi import APIRouter


users_router = APIRouter(prefix="/users")


from . import models  # type: ignore # isort:skip # noqa
