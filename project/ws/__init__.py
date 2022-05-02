from fastapi import APIRouter


ws_router = APIRouter()


from project.ws import views  # type: ignore # isort:skip # noqa
