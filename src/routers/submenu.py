from typing import Union

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import schemas
from database import get_db
from layers.service_layer import SubmenuService

router = APIRouter(
    prefix='/api/v1/menus',
    # API grouping in built-in Swagger UI
    tags=['Подменю']
)

responses = {
    404: {'description': 'Подменю не найдено'},
}


@router.get('/{menu_id}/submenus', response_model=list[schemas.SubmenuCount])
def get_submenus(menu_id: int, db: Session = Depends(get_db)) -> list[schemas.SubmenuCount]:
    serv = SubmenuService()
    return serv.get_all(menu_id, db)


@router.post('/{menu_id}/submenus', status_code=status.HTTP_201_CREATED, response_model=schemas.SubmenuCount)
def create_submenu(menu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)) -> schemas.SubmenuCount:
    serv = SubmenuService()
    return serv.create(menu_id, submenu, db)


@router.get('/{menu_id}/submenus/{submenu_id}', response_model=Union[schemas.SubmenuCount, list[schemas.SubmenuCount]], responses={**responses})
def get_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> list[schemas.SubmenuCount]:
    serv = SubmenuService()
    return serv.get_by_id(menu_id, submenu_id, db)


@router.patch('/{menu_id}/submenus/{submenu_id}', response_model=schemas.SubmenuCount, responses={**responses})
def patch_submenu(menu_id: int, submenu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)) -> schemas.SubmenuCount:
    serv = SubmenuService()
    return serv.update(menu_id, submenu_id, submenu, db)


@router.delete('/{menu_id}/submenus/{submenu_id}', responses={**responses})
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> None:
    serv = SubmenuService()
    serv.delete(menu_id, submenu_id, db)
