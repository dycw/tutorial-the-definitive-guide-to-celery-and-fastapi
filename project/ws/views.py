from json import dumps
from json import loads
from typing import Any

from beartype import beartype
from fastapi import FastAPI
from fastapi import WebSocket
from socketio import ASGIApp
from socketio import AsyncRedisManager
from socketio import AsyncServer
from socketio import RedisManager
from socketio.asyncio_namespace import AsyncNamespace

from project import broadcast
from project.celery_utils import get_task_info
from project.config import settings
from project.ws import ws_router


@ws_router.websocket("/ws/task_status/{task_id}")
@beartype
async def ws_task_status(websocket: WebSocket) -> None:
    await websocket.accept()

    task_id = websocket.scope["path_params"]["task_id"]

    async with broadcast.subscribe(channel=task_id) as subscriber:
        # just in case the task already finish
        data = get_task_info(task_id)
        await websocket.send_json(data)

        async for event in subscriber:
            await websocket.send_json(loads(event.message))


@beartype
async def update_celery_task_status(task_id: str) -> None:
    """
    This function is called by Celery worker in task_postrun signal handler
    """

    await broadcast.connect()
    await broadcast.publish(
        channel=task_id,
        message=dumps(
            get_task_info(task_id)
        ),  # RedisProtocol.publish expect str
    )
    await broadcast.disconnect()


class TaskStatusNameSpace(AsyncNamespace):
    @beartype
    async def on_joina(self, sid: int, data: dict[str, Any]) -> None:
        task_id = data["task_id"]
        self.enter_room(sid=sid, room=task_id)
        # just in case the task already finish
        await self.emit("status", data=get_task_info(task_id), room=task_id)


@beartype
def register_socketio_app(app: FastAPI) -> None:
    mgr = AsyncRedisManager(settings.WS_MESSAGE_QUEUE)
    # https://python-socketio.readthedocs.io/en/latest/server.html#uvicorn-daphne-and-other-asgi-servers
    # https://github.com/tiangolo/fastapi/issues/129#issuecomment-714636723
    sio = AsyncServer(
        async_mode="asgi", client_manager=mgr, logger=True, engineio_logger=True
    )
    sio.register_namespace(TaskStatusNameSpace("/task_status"))
    asgi = ASGIApp(socketio_server=sio)
    app.mount("/ws", asgi)


@beartype
def update_celery_task_status_socketio(task_id: str) -> None:
    """
    This function would be called in Celery worker
    https://python-socketio.readthedocs.io/en/latest/server.html#emitting-from-external-processes
    """

    # connect to the redis queue as an external process
    external_sio = RedisManager(settings.WS_MESSAGE_QUEUE, write_only=True)
    # emit an event
    external_sio.emit(
        "status", get_task_info(task_id), room=task_id, namespace="/task_status"
    )
