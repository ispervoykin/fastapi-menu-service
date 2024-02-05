from typing import Any

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from layers.repository_utils import (
    add_children_to_menu,
    add_children_to_submenu,
    add_to_db,
    check_if_object_exists,
    delete_object,
    get_object,
    update_object,
)
from models import Dish, Menu, Submenu
from schemas import DishCreate, MenuCreate, SubmenuCreate


class MenuRepository():
    def create(self, menu: MenuCreate, db: Session = Depends(get_db)) -> Menu:
        """Создаёт меню в бд"""
        db_menu = Menu(title=menu.title, description=menu.description)

        return add_to_db(db_menu, db)

    def get_all(self, db: Session = Depends(get_db)) -> list[Menu]:
        """Получает все меню из бд"""
        db_menus = db.query(Menu).all()
        for i in range(len(db_menus)):
            db_menus[i] = add_children_to_menu(db_menus[i], db)

        return db_menus

    def get_by_id(self, menu_id: int, db: Session = Depends(get_db)) -> Menu:
        """Получает меню по id из бд"""
        db_menu = get_object(Menu, menu_id, db)

        return add_children_to_menu(db_menu, db)

    def update(self, menu_id: int, menu: MenuCreate, db: Session = Depends(get_db)) -> Menu:
        """Изменяет меню по id в бд"""
        db_menu = get_object(Menu, menu_id, db)

        return update_object(db_menu, menu, db)

    def delete(self, menu_id: int, db: Session = Depends(get_db)) -> None:
        """Удаляет меню по id из бд"""
        delete_object(Menu, menu_id, db)
        return


class SubmenuRepository:
    def create(self, menu_id: int, submenu: SubmenuCreate, db: Session = Depends(get_db)) -> Submenu:
        """Создаёт подменю в бд"""
        check_if_object_exists(Menu, menu_id, db)

        db_submenu = Submenu(title=submenu.title, description=submenu.description, menu_id=menu_id)

        return add_to_db(db_submenu, db)

    def get_all(self, menu_id: int, db: Session = Depends(get_db)) -> list[Submenu]:
        """Получает все подменю из бд"""
        try:
            check_if_object_exists(Menu, menu_id, db)
        except HTTPException:
            return []

        db_submenus = db.query(Submenu).filter(Submenu.menu_id == menu_id).all()
        for i in range(len(db_submenus)):
            db_submenus[i] = add_children_to_submenu(db_submenus[i], db)

        return db_submenus

    def get_by_id(self, menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> Submenu | list[Any]:
        """Получает подменю по id из бд"""
        check_if_object_exists(Menu, menu_id, db)

        db_submenu = get_object(Submenu, submenu_id, db)

        return add_children_to_submenu(db_submenu, db)

    def update(self, menu_id: int, submenu_id: int, submenu: SubmenuCreate, db: Session = Depends(get_db)) -> Submenu:
        """Изменяет подменю по id в бд"""
        check_if_object_exists(Menu, menu_id, db)

        db_submenu = get_object(Submenu, submenu_id, db)

        return update_object(db_submenu, submenu, db)

    def delete(self, menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> None:
        """Удаляет подменю по id из бд"""
        check_if_object_exists(Menu, menu_id, db)

        delete_object(Submenu, submenu_id, db)
        return


class DishRepository:
    def create(self, menu_id: int, submenu_id: int, dish: DishCreate, db: Session = Depends(get_db)) -> Dish:
        """Создаёт блюдо в бд"""
        check_if_object_exists(Menu, menu_id, db)

        check_if_object_exists(Submenu, submenu_id, db)

        db_dish = Dish(title=dish.title, description=dish.description, price=dish.price, submenu_id=submenu_id)

        return add_to_db(db_dish, db)

    def get_all(self, menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> list[Dish]:
        """Получает все блюда из бд"""
        try:
            check_if_object_exists(Menu, menu_id, db)
            check_if_object_exists(Submenu, submenu_id, db)
        except HTTPException:
            return []

        db_dishes = db.query(Dish).filter(Dish.submenu_id == submenu_id).all()
        for i in range(len(db_dishes)):
            db_dishes[i] = db_dishes[i].stringify()

        return db_dishes

    def get_by_id(self, menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)) -> Dish | list[Any]:
        """Получает блюдо по id из бд"""
        check_if_object_exists(Menu, menu_id, db)

        check_if_object_exists(Submenu, submenu_id, db)

        return get_object(Dish, dish_id, db)

    def update(self, menu_id: int, submenu_id: int, dish_id: int, dish: DishCreate, db: Session = Depends(get_db)) -> Dish:
        """Изменяет блюдо по id в бд"""
        check_if_object_exists(Menu, menu_id, db)

        check_if_object_exists(Submenu, submenu_id, db)

        db_dish = get_object(Dish, dish_id, db)

        return update_object(db_dish, dish, db)

    def delete(self, menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)) -> None:
        """Удаляет блюдо по id из бд"""
        check_if_object_exists(Menu, menu_id, db)

        check_if_object_exists(Submenu, submenu_id, db)

        delete_object(Dish, dish_id, db)
        return
