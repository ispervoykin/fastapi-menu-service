from pydantic import BaseModel, Field


class MenuCreate(BaseModel):
    title: str
    description: str


class Menu(MenuCreate):
    id: str


class MenuCount(Menu):
    submenus_count: int = Field(default=0)
    dishes_count: int = Field(default=0)


class SubmenuCreate(BaseModel):
    title: str
    description: str


class Submenu(SubmenuCreate):
    id: str


class SubmenuCount(Submenu):
    dishes_count: int = Field(default=0)


class DishCreate(BaseModel):
    title: str
    description: str
    price: str


class Dish(DishCreate):
    id: str
