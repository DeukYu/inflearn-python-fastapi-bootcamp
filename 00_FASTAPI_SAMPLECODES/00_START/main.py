import asyncio
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import asynccontextmanager

DATABASE_URL = "mysql+aiomysql://ldy8070:deukyu@localhost/db_name"

engine = create_async_engine(DATABASE_URL, echo=True)

ASYNC_SESSION = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=app_lifespan)


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
