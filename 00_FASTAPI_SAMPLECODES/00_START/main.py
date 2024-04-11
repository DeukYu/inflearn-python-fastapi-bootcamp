from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/hello")
def read_hello():
    return {"message": "hi, World!"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item:id": item_id}


@app.get("/getdata/")
def read_items(data: str = "encoding"):
    return {"data": data}


@app.get("/inherit")
def template_inherit(request: Request):
    my_text = "FastAPI와 Jinja2를 이용한 예시입니다."
    return templates.TemplateResponse(
        "index.html", {"request": request, "text": my_text}
    )
