from fastapi import FastAPI
from database import engine
from models import Base
from routers import menu, submenu, dish


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(menu.router)
app.include_router(submenu.router)
app.include_router(dish.router)

