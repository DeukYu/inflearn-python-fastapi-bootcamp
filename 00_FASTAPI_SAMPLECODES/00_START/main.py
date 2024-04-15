from typing import List
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str = Field(..., title="Item Name", min_length=2, max_length=50)
    description: str = Field(
        None, description="The description of the item", max_length=300
    )
    price: float
    tax: float = 0.1
    image: Image


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/hello")
def read_hello():
    return {"message": "hi, World!"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item:id": item_id}


@app.get("/items/")
async def read_items(items: List[int] = Query([])):
    return {"items": items}


@app.get("/getdata/")
def read_data(data: str = "funcoding"):
    return {"data": data}


@app.get("/inherit")
def template_inherit(request: Request):
    my_text = "FastAPI와 Jinja2를 이용한 예시입니다."
    return templates.TemplateResponse(
        "index.html", {"request": request, "text": my_text}
    )


@app.post("/items/")
def create_item(item: Item):
    return {"item": item.model_dump()}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    return {"item_id": item_id, "updated_item": item}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} has been deleted."}
