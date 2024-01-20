from pydantic import BaseModel

class MenuCreate(BaseModel):
    title: str
    description: str

class Menu(MenuCreate):
    id: str

class MenuCount(Menu):
    submenus_count: int
    dishes_count: int

class SubmenuCreate(BaseModel):
    title: str
    description: str

class Submenu(SubmenuCreate):
    id: str

class SubmenuCount(Submenu):
    dishes_count: int

class DishCreate(BaseModel):
    title: str
    description: str
    price: str

class Dish(DishCreate):
    id: str
