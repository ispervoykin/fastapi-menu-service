from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy import func
from database import get_db
from sqlalchemy.orm import Session
from typing import List
from models import Menu, Submenu, Dish
import schemas

router = APIRouter(
    prefix="/api/v1/menus",
    # API grouping in built-in Swagger UI
    tags=['submenus']
)

@router.get("/{menu_id}/submenus", response_model=List[schemas.Submenu])
def get_submenus(menu_id: int, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        return []
    
    db_submenus = db.query(Submenu).filter(Submenu.menu_id == menu_id).all()
    for submenu in db_submenus:
        submenu.id = str(submenu.id)

    return db_submenus

@router.post("/{menu_id}/submenus", status_code=status.HTTP_201_CREATED, response_model=schemas.Submenu)
def create_submenu(menu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="menu not found")

    db_submenu = Submenu(title=submenu.title, description=submenu.description, menu_id=menu_id)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    db_submenu.id = str(db_submenu.id)
    return db_submenu

@router.get("/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubmenuCount)
def get_submenu(menu_id: int, submenu_id: int,  db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        return []
    
    db_submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    if not db_submenu:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="submenu not found")
    
    db_submenu.dishes_count = db.query(func.count(Dish.id)).filter(Dish.submenu_id == db_submenu.id).scalar()

    db_submenu.id = str(db_submenu.id)

    return db_submenu

@router.patch("/{menu_id}/submenus/{submenu_id}", response_model=schemas.Submenu)
def patch_submenu(menu_id: int, submenu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
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

@router.delete("/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="menu not found")
    
    db_submenu_query = db.query(Submenu).filter(Submenu.id == submenu_id)
    if not db_submenu_query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="submenu not found")
    
    db_submenu_query.delete(synchronize_session=False)  
    db.commit()
    return