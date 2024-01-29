from fastapi import FastAPI
from database import engine
from models import Base
from fastapi.middleware.cors import CORSMiddleware
from routers import menu, submenu, dish


app = FastAPI()
Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(menu.router)
app.include_router(submenu.router)
app.include_router(dish.router) 

