from typing import List
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "mysql-pymysql://id:password@localhost/db_name"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class tbl_account(Base):
    __tablename__ = "tbl_account"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(120))


class UserCreate(BaseModel):
    username: str
    email: str


# Base.metadata.create_all(bind=engine)


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


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
def read_root(req: Request):
    return templates.TemplateResponse(
        "index.html", {"request": req, "username": "Deuk Yu"}
    )


# @app.post("/users/")
# def create_user(user : UserCreate, db: Session = Depends(get_db)):
#     new_user = User()


@app.get("/hello")
def read_hello():
    return {"message": "hi, World!"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    try:
        if item_id < 0:
            raise ValueError("음수는 허용되지 않습니다.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


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
