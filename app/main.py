from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False


@app.get("/")
def read_root() -> JSONResponse:
    return JSONResponse({"Hello": "World"})


@app.get("/items/{item_id}")
def read_item(*, item_id: int, q: str | None = None) -> JSONResponse:
    return JSONResponse({"item_id": item_id, "q": q})


@app.put("/items/{item_id}")
def update_item(*, item_id: int, item: Item) -> JSONResponse:
    return JSONResponse({"item_name": item.name, "item_id": item_id})
