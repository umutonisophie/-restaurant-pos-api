from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.menu import CategoryCreate, CategoryOut, MenuItemCreate, MenuItemUpdate, MenuItemOut
from app.services import menu_service

router = APIRouter(prefix="/menu", tags=["menu"])


@router.post("/categories", response_model=CategoryOut, status_code=201)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    return menu_service.create_category(db, payload.name)


@router.get("/categories", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return menu_service.list_categories(db)


@router.get("/categories/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return menu_service.get_category_or_404(db, category_id)


@router.post("/items", response_model=MenuItemOut, status_code=201)
def create_menu_item(payload: MenuItemCreate, db: Session = Depends(get_db)):
    return menu_service.create_menu_item(
        db, payload.name, payload.price, payload.category_id, payload.available
    )


@router.get("/items", response_model=List[MenuItemOut])
def list_menu_items(db: Session = Depends(get_db)):
    return menu_service.list_menu_items(db)


@router.get("/items/{item_id}", response_model=MenuItemOut)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    return menu_service.get_menu_item_or_404(db, item_id)


@router.patch("/items/{item_id}", response_model=MenuItemOut)
def update_menu_item(item_id: int, payload: MenuItemUpdate, db: Session = Depends(get_db)):
    return menu_service.update_menu_item(
        db, item_id,
        name=payload.name, price=payload.price,
        category_id=payload.category_id, available=payload.available,
    )
