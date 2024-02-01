from fastapi import Depends, status, HTTPException
from database import get_db
from sqlalchemy import distinct, func
from models import Menu, Dish, Submenu
from sqlalchemy.orm import Session
import schemas


class MenuRepository:
    def create(self, menu: schemas.MenuCreate, db: Session = Depends(get_db)):
        db_menu = Menu(title=menu.title, description=menu.description)
        db.add(db_menu)
        db.commit()
        db.refresh(db_menu)
        db_menu.id = str(db_menu.id)
        return db_menu

    def get_all(self, db: Session = Depends(get_db)):
        db_menus = db.query(Menu).all() 
        for menu in db_menus:
            menu.id = str(menu.id)
            query = db.query(
                    func.count(distinct(Submenu.id)).label("submenus_count"),
                    func.count(Dish.id).label("dishes_count")
                    )\
                    .outerjoin(Dish, Submenu.id == Dish.submenu_id)\
                    .filter(Submenu.menu_id == menu.id)\
                    .first()

            menu.submenus_count = query.submenus_count
            menu.dishes_count = query.dishes_count

        return db_menus
    
    def get_by_id(self, menu_id: int, db: Session = Depends(get_db)):
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="menu not found")

        query = db.query(
                func.count(distinct(Submenu.id)).label("submenus_count"),
                func.count(Dish.id).label("dishes_count")
                )\
                .outerjoin(Dish, Submenu.id == Dish.submenu_id)\
                .filter(Submenu.menu_id == db_menu.id)\
                .first()

        db_menu.submenus_count = query.submenus_count
        db_menu.dishes_count = query.dishes_count

        db_menu.id = str(db_menu.id)
        return db_menu

    def update(self, menu_id: int, menu: schemas.MenuCreate, db: Session = Depends(get_db)):
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="menu not found")
        menu_dump = menu.model_dump()
        for key in menu_dump.keys():
            setattr(db_menu, key, menu_dump[key])
        db.commit()
        db_menu.id = str(db_menu.id)
        return db_menu

    def delete(self, menu_id: int, db: Session = Depends(get_db)):
        db_menu_query = db.query(Menu).filter(Menu.id == menu_id)
        if not db_menu_query.first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="menu not found")
        
        db_menu_query.delete(synchronize_session=False)  
        db.commit()
        return
    
class SubmenuRepository:
    def create(self, menu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="menu not found")

        db_submenu = Submenu(title=submenu.title, description=submenu.description, menu_id=menu_id)
        db.add(db_submenu)
        db.commit()
        db.refresh(db_submenu)
        db_submenu.id = str(db_submenu.id)
        return db_submenu

    def get_all(self, menu_id: int, db: Session = Depends(get_db)):
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            return []
        
        db_submenus = db.query(Submenu).filter(Submenu.menu_id == menu_id).all()
        for submenu in db_submenus:
            submenu.id = str(submenu.id)

        return db_submenus
    
    def get_by_id(self, menu_id: int, submenu_id: int,  db: Session = Depends(get_db)):
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            return []
        
        db_submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
        if not db_submenu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="submenu not found")
        
        db_submenu.dishes_count = db.query(func.count(Dish.id)).filter(Dish.submenu_id == db_submenu.id).scalar()

        db_submenu.id = str(db_submenu.id)

        return db_submenu

    def update(self, menu_id: int, submenu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="menu not found")
        
        db_submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
        if not db_submenu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="submenu not found")

        submenu_dump = submenu.model_dump()
        for key in submenu_dump.keys():
            setattr(db_submenu, key, submenu_dump[key])

        db.commit()
        db_submenu.id = str(db_submenu.id)
        return db_submenu

    def delete(self, menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="menu not found")
        
        db_submenu_query = db.query(Submenu).filter(Submenu.id == submenu_id)
        if not db_submenu_query.first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="submenu not found")
        
        db_submenu_query.delete(synchronize_session=False)  
        db.commit()
        return
    
class DishRepository:
    def create(self, menu_id: int, submenu_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)):
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="menu not found")
        
        db_submenu = db.query(Menu).join(Submenu).filter(Submenu.id == submenu_id).first()
        if not db_submenu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="submenu not found")

        db_dish = Dish(title=dish.title, description=dish.description, price=dish.price, submenu_id=submenu_id)
        db.add(db_dish)
        db.commit()
        db.refresh(db_dish)
        db_dish.id = str(db_dish.id)
        db_dish.price = str(db_dish.price)
        return db_dish

    def get_all(self, menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            return []
        
        db_submenu = db.query(Menu).join(Submenu).filter(Submenu.id == submenu_id).first()
        if not db_submenu:
            return []
        
        db_dishes = db.query(Dish).filter(Dish.submenu_id == submenu_id).all()
        for dish in db_dishes:
            dish.id = str(dish.id)
            dish.price = str(dish.price)

        return db_dishes
    
    def get_by_id(self, menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            return []
        
        db_submenu = db.query(Menu).join(Submenu).filter(Submenu.id == submenu_id).first()
        if not db_submenu:
            return []

        db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
        if not db_dish:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="dish not found")
        
        db_dish.id = str(db_dish.id)
        db_dish.price = str(db_dish.price)

        return db_dish

    def update(self, menu_id: int, submenu_id: int, dish_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)):
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="menu not found")
        
        db_submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
        if not db_submenu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="submenu not found")

        db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
        if not db_dish:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="dish not found")

        dish_dump = dish.model_dump()
        for key in dish_dump.keys():
            setattr(db_dish, key, dish_dump[key])

        db.commit()
        db_dish.id = str(db_dish.id)
        db_dish.price = str(db_dish.price)
        return db_dish

    def delete(self, menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="menu not found")
        
        db_submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
        if not db_submenu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="submenu not found")

        db_dish_query = db.query(Dish).filter(Dish.id == dish_id)
        if not db_dish_query.first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="dish not found")
        
        db_dish_query.delete(synchronize_session=False)  
        db.commit()
        return