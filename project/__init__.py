from beartype import beartype
from broadcaster import Broadcast
from fastapi import FastAPI

from project.config import settings


broadcast = Broadcast(settings.WS_MESSAGE_QUEUE)


@beartype
def create_app() -> FastAPI:
    app = FastAPI()

    # do this before loading routes
    from project.celery_utils import create_celery

    app.celery_app = create_celery()  # type: ignore

    # routers
    from project.users import users_router

    app.include_router(users_router)

    # routers
    from project.ws import ws_router

    app.include_router(ws_router)

    @app.on_event("startup")  # type: ignore
    async def startup_event() -> None:  # type: ignore
        await broadcast.connect()

    @app.on_event("shutdown")  # type: ignore
    async def shutdown_event() -> None:  # type: ignore
        await broadcast.disconnect()

    @app.get("/")
    async def root() -> dict[str, str]:  # type: ignore
        return {"message": "Hello World"}

    return app
