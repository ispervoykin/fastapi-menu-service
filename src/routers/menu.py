from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy import distinct, func
from database import get_db
from sqlalchemy.orm import Session
from typing import List
from models import Menu, Submenu, Dish
import schemas as schemas


router = APIRouter(
    prefix="/api/v1/menus",
    # API grouping in built-in Swagger UI
    tags=['menus']
)

@router.get("/", response_model=List[schemas.MenuCount])
def get_menus(db: Session = Depends(get_db)):
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

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Menu)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu = Menu(title=menu.title, description=menu.description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    db_menu.id = str(db_menu.id)
    return db_menu

@router.get("/{menu_id}", status_code=status.HTTP_200_OK, response_model=schemas.MenuCount)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
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

@router.patch("/{menu_id}", response_model=schemas.Menu)
def patch_menu(menu_id: int, menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="menu not found")
    menu_dump = menu.model_dump()
    for key in menu_dump.keys():
        setattr(db_menu, key, menu_dump[key])
    db.commit()
    db_menu.id = str(db_menu.id)
    return db_menu

@router.delete("/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu_query = db.query(Menu).filter(Menu.id == menu_id)
    if not db_menu_query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="menu not found")
    
    db_menu_query.delete(synchronize_session=False)  
    db.commit()
    return