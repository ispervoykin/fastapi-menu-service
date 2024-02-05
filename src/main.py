from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from init_redis import redis_db
from models import Base
from routers import dish, menu, submenu


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    redis_db.flushdb(asynchronous=True)

app = FastAPI(lifespan=lifespan)

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(menu.router)
app.include_router(submenu.router)
app.include_router(dish.router)
