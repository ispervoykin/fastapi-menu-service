from typing import Union

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import schemas as schemas
from database import get_db
from layers.service import DishService

router = APIRouter(
    prefix='/api/v1/menus',
    # API grouping in built-in Swagger UI
    tags=['dishes']
)


@router.get('/{menu_id}/submenus/{submenu_id}/dishes', response_model=list[schemas.Dish])
def get_dishes(menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> list[schemas.Dish]:
    serv = DishService()
    return serv.get_all(menu_id, submenu_id, db)


@router.post('/{menu_id}/submenus/{submenu_id}/dishes', status_code=status.HTTP_201_CREATED, response_model=schemas.Dish)
def create_dish(menu_id: int, submenu_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)) -> schemas.Dish:
    serv = DishService()
    return serv.create(menu_id, submenu_id, dish, db)


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=Union[schemas.Dish, list[schemas.Dish]])
def get_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)) -> schemas.Dish | list[schemas.Dish]:
    serv = DishService()
    return serv.get_by_id(menu_id, submenu_id, dish_id, db)


@router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=schemas.Dish)
def patch_dish(menu_id: int, submenu_id: int, dish_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)) -> schemas.Dish:
    serv = DishService()
    return serv.update(menu_id, submenu_id, dish_id, dish, db)


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)) -> None:
    serv = DishService()
    serv.delete(menu_id, submenu_id, dish_id, db)
