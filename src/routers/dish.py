from fastapi import Depends, status, HTTPException, APIRouter
from database import get_db
from sqlalchemy.orm import Session
from typing import List
from models import Menu, Submenu, Dish
import schemas as schemas

router = APIRouter(
    prefix="/api/v1/menus",
    # API grouping in built-in Swagger UI
    tags=['dishes']
)

@router.get("/{menu_id}/submenus/{submenu_id}/dishes", response_model=List[schemas.Dish])
def get_dishes(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        return []
    
    db_submenu = db.query(Menu).filter(Submenu.id == submenu_id).first()
    if not db_submenu:
        return []
    
    db_dishes = db.query(Dish).filter(Dish.submenu_id == submenu_id).all()
    for dish in db_dishes:
        dish.id = str(dish.id)
        dish.price = str(dish.price)

    return db_dishes

@router.post("/{menu_id}/submenus/{submenu_id}/dishes", status_code=status.HTTP_201_CREATED, response_model=schemas.Dish)
def create_dish(menu_id: int, submenu_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="menu not found")
    
    db_submenu = db.query(Menu).filter(Submenu.id == submenu_id).first()
    if not db_submenu:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="submenu not found")

    db_dish = Dish(title=dish.title, description=dish.description, price=dish.price, submenu_id=submenu_id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    db_dish.id = str(db_dish.id)
    db_dish.price = str(db_dish.price)
    return db_dish

@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def get_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        return []
    
    db_submenu = db.query(Menu).filter(Submenu.id == submenu_id).first()
    if not db_submenu:
        return []

    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not db_dish:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="dish not found")
    
    db_dish.id = str(db_dish.id)
    db_dish.price = str(db_dish.price)

    return db_dish

@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def patch_dish(menu_id: int, submenu_id: int, dish_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)):
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

@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
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