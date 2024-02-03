from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import schemas
from database import get_db
from layers.service import MenuService

router = APIRouter(
    prefix='/api/v1/menus',
    # API grouping in built-in Swagger UI
    tags=['menus']
)


@router.get('/', response_model=list[schemas.MenuCount])
def get_menus(db: Session = Depends(get_db)) -> list[schemas.MenuCount]:
    serv = MenuService()
    return serv.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Menu)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)) -> schemas.Menu:
    serv = MenuService()
    return serv.create(menu, db)


@router.get('/{menu_id}', status_code=status.HTTP_200_OK, response_model=schemas.MenuCount)
def get_menu(menu_id: int, db: Session = Depends(get_db)) -> schemas.MenuCount:
    serv = MenuService()
    return serv.get_by_id(menu_id, db)


@router.patch('/{menu_id}', response_model=schemas.Menu)
def patch_menu(menu_id: int, menu: schemas.MenuCreate, db: Session = Depends(get_db)) -> schemas.Menu:
    serv = MenuService()
    return serv.update(menu_id, menu, db)


@router.delete('/{menu_id}')
def delete_menu(menu_id: int, db: Session = Depends(get_db)) -> None:
    serv = MenuService()
    serv.delete(menu_id, db)
