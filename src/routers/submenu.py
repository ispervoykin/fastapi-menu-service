from fastapi import Depends, status, APIRouter
from database import get_db
from sqlalchemy.orm import Session
from typing import List
from layers.service import SubmenuService
import schemas

router = APIRouter(
    prefix="/api/v1/menus",
    # API grouping in built-in Swagger UI
    tags=['submenus']
)

@router.get("/{menu_id}/submenus", response_model=List[schemas.Submenu])
def get_submenus(menu_id: int, db: Session = Depends(get_db)):
    serv = SubmenuService()
    return serv.get_all(menu_id, db)

@router.post("/{menu_id}/submenus", status_code=status.HTTP_201_CREATED, response_model=schemas.Submenu)
def create_submenu(menu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
    serv = SubmenuService()
    return serv.create(menu_id, submenu, db)

@router.get("/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubmenuCount)
def get_submenu(menu_id: int, submenu_id: int,  db: Session = Depends(get_db)):
    serv = SubmenuService()
    return serv.get_by_id(menu_id, submenu_id, db)

@router.patch("/{menu_id}/submenus/{submenu_id}", response_model=schemas.Submenu)
def patch_submenu(menu_id: int, submenu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
    serv = SubmenuService()
    return serv.update(menu_id, submenu_id, submenu, db)

@router.delete("/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    serv = SubmenuService()
    return serv.delete(menu_id, submenu_id, db)