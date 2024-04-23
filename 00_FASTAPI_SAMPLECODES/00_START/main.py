import asyncio
from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware

DATABASE_URL = "mysql+aiomysql://ldy8070:deukyu@localhost/db_name"

engine = create_async_engine(DATABASE_URL, echo=True)

ASYNC_SESSION = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()


# @asynccontextmanager
# async def app_lifespan(app: FastAPI):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield


app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="secret_key")


@app.post("/set/")
async def set_session(request: Request):
    request.session["username"] = "john"
    return {"message": "Session value set"}


@app.get("/get/")
async def get_session(request: Request):
    username = request.session.get("username", "Guest")
    return {"username": username}


async def get_db():
    async with ASYNC_SESSION() as session:
        yield session
        await session.commit()


async def fetch_data():
    await asyncio.sleep(2)
    return {"data": "some_data"}


@app.get("/")
async def read_root():
    data = await fetch_data()
    return {"message": "Hello, World!", "fetched_data": data}
