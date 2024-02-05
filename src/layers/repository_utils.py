from fastapi import HTTPException, status
from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

from models import Dish, Menu, Submenu
from schemas import DishCreate, MenuCreate, SubmenuCreate


def get_object(model: Menu | Submenu | Dish, id: int, db: Session) -> Menu | Submenu | Dish:
    """Получает объект указанной модели из дб. Если его нет - кидает исключение."""
    db_object = db.query(model).filter(model.id == id).first()
    if not db_object:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'{str(model())} not found')
    return db_object


def check_if_object_exists(model: Menu | Submenu | Dish, id: int, db: Session) -> None:
    """Проверяет наличие объекта указанной модели в дб. Если его нет - кидает исключение."""
    db_object = db.query(model).filter(model.id == id).first()
    if not db_object:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'{str(model())} not found')
    return


def add_to_db(object: Menu | Submenu | Dish, db: Session) -> Menu | Submenu | Dish:
    """Добавляет объект указанной модели в бд."""
    db.add(object)
    db.commit()
    db.refresh(object)
    object = object.stringify()
    return object


def add_children_to_menu(menu: Menu, db: Session) -> Menu:
    """Добавляет в меню количество связанных подменю и блюд"""
    query = db.query(
        func.count(distinct(Submenu.id)).label('submenus_count'),
        func.count(Dish.id).label('dishes_count')
    )\
        .outerjoin(Dish, Submenu.id == Dish.submenu_id)\
        .filter(Submenu.menu_id == menu.id)\
        .first()

    menu.submenus_count = query.submenus_count
    menu.dishes_count = query.dishes_count

    menu = menu.stringify()
    return menu


def add_children_to_submenu(submenu: Submenu, db: Session) -> Submenu:
    """Добавляет в подменю количество связанных блюд"""
    query = db.query(func.count(Dish.id)).filter(Dish.submenu_id == submenu.id).scalar()

    submenu.dishes_count = query

    submenu = submenu.stringify()
    return submenu


def update_object(object: Menu | Submenu | Dish, model: MenuCreate | SubmenuCreate | DishCreate, db: Session):
    """Обновляет объект"""
    model_dump = model.model_dump()
    for key in model_dump.keys():
        setattr(object, key, model_dump[key])

    db.commit()
    object = object.stringify()
    return object


def delete_object(model: Menu | Submenu | Dish, id: int, db: Session) -> None:
    """Удаляет объект из бд"""
    object_query = db.query(model).filter(model.id == id)
    if not object_query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'{str(model())} not found')

    object_query.delete(synchronize_session=False)
    db.commit()
    return
