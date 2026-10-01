from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories import menu_repository


def create_category(db: Session, name: str):
    return menu_repository.create_category(db, name)


def list_categories(db: Session):
    return menu_repository.list_categories(db)


def get_category_or_404(db: Session, category_id: int):
    category = menu_repository.get_category(db, category_id)
    if not category:
        raise HTTPException(404, "Category not found")
    return category


def create_menu_item(db: Session, name: str, price: float, category_id: int, available: bool):
    category = menu_repository.get_category(db, category_id)
    if not category:
        raise HTTPException(404, "Category not found")
    return menu_repository.create_menu_item(db, name, price, category_id, available)


def list_menu_items(db: Session):
    return menu_repository.list_menu_items(db)


def get_menu_item_or_404(db: Session, item_id: int):
    item = menu_repository.get_menu_item(db, item_id)
    if not item:
        raise HTTPException(404, "Menu item not found")
    return item


def update_menu_item(db: Session, item_id: int, **kwargs):
    item = get_menu_item_or_404(db, item_id)
    return menu_repository.update_menu_item(db, item, **kwargs)
