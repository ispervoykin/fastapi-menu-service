from typing import Any

from fastapi import Depends, HTTPException, status
from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

import schemas
from database import get_db
from models import Dish, Menu, Submenu


def add_to_db(object: Menu, db: Session) -> None:
    db.add(object)
    db.commit()
    db.refresh(object)


class MenuRepository():
    def create(self, menu: schemas.MenuCreate, db: Session = Depends(get_db)) -> dict[str, str]:
        """Создаёт меню в бд"""
        db_menu = Menu(title=menu.title, description=menu.description)
        add_to_db(db_menu, db)

        db_menu = db_menu.stringify()

        return db_menu

    def get_all(self, db: Session = Depends(get_db)) -> list[Menu]:
        """Получает все меню из бд"""
        db_menus = db.query(Menu).all()
        for i in range(len(db_menus)):
            query = db.query(
                func.count(distinct(Submenu.id)).label('submenus_count'),
                func.count(Dish.id).label('dishes_count')
            )\
                .outerjoin(Dish, Submenu.id == Dish.submenu_id)\
                .filter(Submenu.menu_id == db_menus[i].id)\
                .first()

            db_menus[i].submenus_count = query.submenus_count
            db_menus[i].dishes_count = query.dishes_count

            db_menus[i] = db_menus[i].stringify()

        return db_menus

    def get_by_id(self, menu_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
        """Получает меню по id из бд"""
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='menu not found')

        query = db.query(
            func.count(distinct(Submenu.id)).label('submenus_count'),
            func.count(Dish.id).label('dishes_count')
        )\
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)\
            .filter(Submenu.menu_id == db_menu.id)\
            .first()

        db_menu.submenus_count = query.submenus_count
        db_menu.dishes_count = query.dishes_count

        db_menu = db_menu.stringify()

        return db_menu

    def update(self, menu_id: int, menu: schemas.MenuCreate, db: Session = Depends(get_db)) -> dict[str, str]:
        """Изменяет меню по id в бд"""
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='menu not found')

        menu_dump = menu.model_dump()
        for key in menu_dump.keys():
            setattr(db_menu, key, menu_dump[key])

        db.commit()

        db_menu = db_menu.stringify()

        return db_menu

    def delete(self, menu_id: int, db: Session = Depends(get_db)) -> None:
        """Удаляет меню по id из бд"""
        db_menu_query = db.query(Menu).filter(Menu.id == menu_id)
        if not db_menu_query.first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='menu not found')

        db_menu_query.delete(synchronize_session=False)
        db.commit()
        return


class SubmenuRepository:
    def create(self, menu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)) -> dict[str, str]:
        """Создаёт подменю в бд"""
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='menu not found')

        db_submenu = Submenu(title=submenu.title, description=submenu.description, menu_id=menu_id)
        add_to_db(db_submenu, db)

        db_submenu = db_submenu.stringify()

        return db_submenu

    def get_all(self, menu_id: int, db: Session = Depends(get_db)) -> list[Submenu]:
        """Получает все подменю из бд"""
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            return []

        db_submenus = db.query(Submenu).filter(Submenu.menu_id == menu_id).all()
        for i in range(len(db_submenus)):
            db_submenus[i] = db_submenus[i].stringify()

        return db_submenus

    def get_by_id(self, menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> dict[str, str] | list[Any]:
        """Получает подменю по id из бд"""
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            return []

        db_submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
        if not db_submenu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='submenu not found')

        db_submenu.dishes_count = db.query(func.count(Dish.id)).filter(Dish.submenu_id == db_submenu.id).scalar()

        db_submenu = db_submenu.stringify()
        return db_submenu

    def update(self, menu_id: int, submenu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)) -> dict[str, str]:
        """Изменяет подменю по id в бд"""
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='menu not found')

        db_submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
        if not db_submenu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='submenu not found')

        submenu_dump = submenu.model_dump()
        for key in submenu_dump.keys():
            setattr(db_submenu, key, submenu_dump[key])

        db.commit()
        db_submenu = db_submenu.stringify()

        return db_submenu

    def delete(self, menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> None:
        """Удаляет подменю по id из бд"""
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='menu not found')

        db_submenu_query = db.query(Submenu).filter(Submenu.id == submenu_id)
        if not db_submenu_query.first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='submenu not found')

        db_submenu_query.delete(synchronize_session=False)
        db.commit()
        return


class DishRepository:
    def create(self, menu_id: int, submenu_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)) -> dict[str, str]:
        """Создаёт блюдо в бд"""
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='menu not found')

        db_submenu = db.query(Menu).join(Submenu).filter(Submenu.id == submenu_id).first()
        if not db_submenu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='submenu not found')

        db_dish = Dish(title=dish.title, description=dish.description, price=dish.price, submenu_id=submenu_id)
        add_to_db(db_dish, db)

        db_dish = db_dish.stringify()
        return db_dish

    def get_all(self, menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> list[Dish]:
        """Получает все блюда из бд"""
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            return []

        db_submenu = db.query(Menu).join(Submenu).filter(Submenu.id == submenu_id).first()
        if not db_submenu:
            return []

        db_dishes = db.query(Dish).filter(Dish.submenu_id == submenu_id).all()
        for i in range(len(db_dishes)):
            db_dishes[i] = db_dishes[i].stringify()

        return db_dishes

    def get_by_id(self, menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)) -> dict[str, str] | list[Any]:
        """Получает блюдо по id из бд"""
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            return []

        db_submenu = db.query(Menu).join(Submenu).filter(Submenu.id == submenu_id).first()
        if not db_submenu:
            return []

        db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
        if not db_dish:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='dish not found')

        db_dish = db_dish.stringify()

        return db_dish

    def update(self, menu_id: int, submenu_id: int, dish_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)) -> dict[str, str]:
        """Изменяет блюдо по id в бд"""
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='menu not found')

        db_submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
        if not db_submenu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='submenu not found')

        db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
        if not db_dish:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='dish not found')

        dish_dump = dish.model_dump()
        for key in dish_dump.keys():
            setattr(db_dish, key, dish_dump[key])

        db.commit()

        db_dish = db_dish.stringify()

        return db_dish

    def delete(self, menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)) -> None:
        """Удаляет блюдо по id из бд"""
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='menu not found')

        db_submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
        if not db_submenu:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='submenu not found')

        db_dish_query = db.query(Dish).filter(Dish.id == dish_id)
        if not db_dish_query.first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='dish not found')

        db_dish_query.delete(synchronize_session=False)
        db.commit()
        return
