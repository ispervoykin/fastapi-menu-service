from fastapi import Depends
from sqlalchemy.orm import Session

import schemas
from database import get_db
from models import Dish, Menu, Submenu

from .redis_layer import DishRedis, MenuRedis, SubmenuRedis
from .repository import DishRepository, MenuRepository, SubmenuRepository


class MenuService:
    def __init__(self):
        self.repository = MenuRepository()
        self.redis = MenuRedis()

    def create(self, menu: schemas.MenuCreate, db: Session = Depends(get_db)) -> dict[str, str]:
        db_menu = self.repository.create(menu, db)
        self.redis.create(db_menu)
        return db_menu

    def get_all(self, db: Session = Depends(get_db)) -> list[Menu]:
        return self.repository.get_all(db)

    def get_by_id(self, menu_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
        cache = self.redis.get(menu_id)
        if cache is not None:
            return cache

        db_menu = self.repository.get_by_id(menu_id, db)
        self.redis.create(db_menu, menu_id)
        return db_menu

    def update(self, menu_id: int, menu: schemas.MenuCreate, db: Session = Depends(get_db)) -> dict[str, str]:
        self.redis.delete(menu_id)

        db_menu = self.repository.update(menu_id, menu, db)
        self.redis.create(db_menu, menu_id)
        return db_menu

    def delete(self, menu_id: int, db: Session = Depends(get_db)) -> None:
        self.redis.delete_children(menu_id)
        self.repository.delete(menu_id, db)


class SubmenuService:
    def __init__(self):
        self.repository = SubmenuRepository()
        self.redis = SubmenuRedis()

    def create(self, menu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)) -> dict[str, str]:
        db_submenu = self.repository.create(menu_id, submenu, db)
        self.redis.create(db_submenu, menu_id)
        return db_submenu

    def get_all(self, menu_id: int, db: Session = Depends(get_db)) -> list[Submenu]:
        print(self.repository.get_all(menu_id, db))
        return self.repository.get_all(menu_id, db)

    def get_by_id(self, menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
        cache = self.redis.get(menu_id, submenu_id)
        if cache is not None:
            return cache

        db_submenu = self.repository.get_by_id(menu_id, submenu_id, db)
        self.redis.create(db_submenu, menu_id, submenu_id)
        return db_submenu

    def update(self, menu_id: int, submenu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)) -> dict[str, str]:
        self.redis.delete(menu_id, submenu_id)

        db_submenu = self.repository.update(menu_id, submenu_id, submenu, db)
        self.redis.create(db_submenu, menu_id, submenu_id)
        return db_submenu

    def delete(self, menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> None:
        self.redis.delete_children(menu_id, submenu_id)
        self.repository.delete(menu_id, submenu_id, db)


class DishService:
    def __init__(self):
        self.repository = DishRepository()
        self.redis = DishRedis()

    def create(self, menu_id: int, submenu_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)) -> dict[str, str]:
        db_dish = self.repository.create(menu_id, submenu_id, dish, db)
        self.redis.create(db_dish, menu_id, submenu_id)
        return db_dish

    def get_all(self, menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> list[Dish]:
        return self.repository.get_all(menu_id, submenu_id, db)

    def get_by_id(self, menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
        cache = self.redis.get(menu_id, submenu_id, dish_id)
        if cache is not None:
            return cache

        db_dish = self.repository.get_by_id(menu_id, submenu_id, dish_id, db)
        self.redis.create(db_dish, menu_id, submenu_id, dish_id)
        return db_dish

    def update(self, menu_id: int, submenu_id: int, dish_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)) -> dict[str, str]:
        self.redis.delete(menu_id, submenu_id, dish_id)

        db_dish = self.repository.update(menu_id, submenu_id, dish_id, dish, db)
        self.redis.create(db_dish, menu_id, submenu_id, dish_id)
        return db_dish

    def delete(self, menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)) -> None:
        self.redis.delete_children(menu_id, submenu_id, dish_id)
        self.repository.delete(menu_id, submenu_id, dish_id, db)
