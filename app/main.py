from celery import Celery
from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI()


celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0",
)


@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse({"message": "Hello World"})


@celery.task(name="app.main.divide")
def divide(x: float, y: float) -> float:
    import time

    time.sleep(3)
    return x / y
