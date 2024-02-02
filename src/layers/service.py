from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session
from .repository import MenuRepository, SubmenuRepository, DishRepository
from .redis_layer import MenuRedis, SubmenuRedis, DishRedis
import schemas
from init_redis import redis_db

class MenuService:
    def __init__(self):
        self.repository = MenuRepository()
        self.redis = MenuRedis()
    
    def create(self, menu: schemas.MenuCreate, db: Session = Depends(get_db)):
        db_menu = self.repository.create(menu, db)
        self.redis.create(db_menu)
        return db_menu
    
    def get_all(self, db: Session = Depends(get_db)):
        return self.repository.get_all(db)

    def get_by_id(self, menu_id: int, db: Session = Depends(get_db)):
        cache = self.redis.get(menu_id)
        if cache is not None:
            return cache
        
        db_menu = self.repository.get_by_id(menu_id, db)
        self.redis.create(db_menu, menu_id)
        return db_menu

    def update(self, menu_id: int, menu: schemas.MenuCreate, db: Session = Depends(get_db)):
        self.redis.delete(menu_id)

        db_menu = self.repository.update(menu_id, menu, db)
        self.redis.create(db_menu, menu_id)
        return db_menu

    def delete(self, menu_id: int, db: Session = Depends(get_db)):
        self.redis.delete_children(menu_id)
        return self.repository.delete(menu_id, db)

class SubmenuService:
    def __init__(self):
        self.repository = SubmenuRepository()
        self.redis = SubmenuRedis()
    
    def create(self, menu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
        db_submenu = self.repository.create(menu_id, submenu, db)
        self.redis.create(db_submenu, menu_id)
        return db_submenu
    
    def get_all(self, menu_id: int, db: Session = Depends(get_db)):
        return self.repository.get_all(menu_id, db)

    def get_by_id(self, menu_id: int, submenu_id: int,  db: Session = Depends(get_db)):
        cache = self.redis.get(menu_id, submenu_id)
        if cache is not None:
            return cache
        
        db_submenu = self.repository.get_by_id(menu_id, submenu_id, db)
        self.redis.create(db_submenu, menu_id, submenu_id)
        return db_submenu

    def update(self, menu_id: int, submenu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
        self.redis.delete(menu_id, submenu_id)
        
        db_submenu = self.repository.update(menu_id, submenu_id, submenu, db)
        self.redis.create(db_submenu, menu_id, submenu_id)
        return db_submenu

    def delete(self, menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
        self.redis.delete_children(menu_id, submenu_id)
        return self.repository.delete(menu_id, submenu_id, db)
    
class DishService:
    def __init__(self):
        self.repository = DishRepository()
        self.redis = DishRedis()
    
    def create(self, menu_id: int, submenu_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)):
        db_dish = self.repository.create(menu_id, submenu_id, dish, db)
        self.redis.create(db_dish, menu_id, submenu_id)
        return db_dish
    
    def get_all(self, menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
        return self.repository.get_all(menu_id, submenu_id, db)

    def get_by_id(self, menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
        cache = self.redis.get(menu_id, submenu_id, dish_id)
        if cache is not None:
            return cache

        db_dish = self.repository.get_by_id(menu_id, submenu_id, dish_id, db)
        self.redis.create(db_dish, menu_id, submenu_id, dish_id)
        return db_dish

    def update(self, menu_id: int, submenu_id: int, dish_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)):
        self.redis.delete(menu_id, submenu_id, dish_id)

        db_dish = self.repository.update(menu_id, submenu_id, dish_id, dish, db)
        self.redis.create(db_dish, menu_id, submenu_id, dish_id)
        return db_dish

    def delete(self, menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
        self.redis.delete_children(menu_id, submenu_id, dish_id)
        return self.repository.delete(menu_id, submenu_id, dish_id, db)