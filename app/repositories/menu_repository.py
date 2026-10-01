from typing import Optional, List
from sqlalchemy.orm import Session, selectinload
from app.models.menu import Category, MenuItem


def create_category(db: Session, name: str) -> Category:
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def list_categories(db: Session) -> List[Category]:
    return db.query(Category).options(selectinload(Category.menu_items)).all()


def get_category(db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).options(
        selectinload(Category.menu_items),
    ).filter(Category.id == category_id).first()


def get_menu_item(db: Session, item_id: int) -> Optional[MenuItem]:
    return db.query(MenuItem).options(
        selectinload(MenuItem.category),
    ).filter(MenuItem.id == item_id).first()


def create_menu_item(db: Session, name: str, price: float, category_id: int, available: bool) -> MenuItem:
    item = MenuItem(name=name, price=price, category_id=category_id, available=available)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_menu_items(db: Session) -> List[MenuItem]:
    return db.query(MenuItem).options(selectinload(MenuItem.category)).all()


def update_menu_item(db: Session, item: MenuItem, **kwargs) -> MenuItem:
    for key, value in kwargs.items():
        if value is not None:
            setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item
