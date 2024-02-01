from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session
from .repository import MenuRepository, SubmenuRepository, DishRepository
import schemas

class MenuService:
    def __init__(self):
        self.repository = MenuRepository()
    
    def create(self, menu: schemas.MenuCreate, db: Session = Depends(get_db)):
        return self.repository.create(menu, db)
    
    def get_all(self, db: Session = Depends(get_db)):
        return self.repository.get_all(db)

    def get_by_id(self, menu_id: int, db: Session = Depends(get_db)):
        return self.repository.get_by_id(menu_id, db)

    def update(self, menu_id: int, menu: schemas.MenuCreate, db: Session = Depends(get_db)):
        return self.repository.update(menu_id, menu, db)

    def delete(self, menu_id: int, db: Session = Depends(get_db)):
        return self.repository.delete(menu_id, db)

class SubmenuService:
    def __init__(self):
        self.repository = SubmenuRepository()
    
    def create(self, menu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
        return self.repository.create(menu_id, submenu, db)
    
    def get_all(self, menu_id: int, db: Session = Depends(get_db)):
        return self.repository.get_all(menu_id, db)

    def get_by_id(self, menu_id: int, submenu_id: int,  db: Session = Depends(get_db)):
        return self.repository.get_by_id(menu_id, submenu_id, db)

    def update(self, menu_id: int, submenu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
        return self.repository.update(menu_id, submenu_id, submenu, db)

    def delete(self, menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
        return self.repository.delete(menu_id, submenu_id, db)
    
class DishService:
    def __init__(self):
        self.repository = DishRepository()
    
    def create(self, menu_id: int, submenu_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)):
        return self.repository.create(menu_id, submenu_id, dish, db)
    
    def get_all(self, menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
        return self.repository.get_all(menu_id, submenu_id, db)

    def get_by_id(self, menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
        return self.repository.get_by_id(menu_id, submenu_id, dish_id, db)

    def update(self, menu_id: int, submenu_id: int, dish_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)):
        return self.repository.update(menu_id, submenu_id, dish_id, dish, db)

    def delete(self, menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
        return self.repository.delete(menu_id, submenu_id, dish_id, db)