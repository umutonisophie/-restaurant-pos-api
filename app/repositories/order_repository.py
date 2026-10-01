from typing import Optional, List
from sqlalchemy.orm import Session, selectinload
from app.models.order import Order, OrderItem, OrderStatus


def create_order(db: Session, table_id: int) -> Order:
    order = Order(table_id=table_id, status=OrderStatus.open)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: int) -> Optional[Order]:
    return db.query(Order).options(
        selectinload(Order.items),
        selectinload(Order.table),
        selectinload(Order.payment),
    ).filter(Order.id == order_id).first()


def list_orders(db: Session) -> List[Order]:
    return db.query(Order).options(
        selectinload(Order.items),
        selectinload(Order.table),
    ).all()


def add_item(db: Session, order_id: int, menu_item_id: int, quantity: int, notes: Optional[str], price: float) -> OrderItem:
    item = OrderItem(
        order_id=order_id, menu_item_id=menu_item_id,
        quantity=quantity, notes=notes, price_at_order_time=price,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def set_status(db: Session, order: Order, status: OrderStatus) -> Order:
    order.status = status
    db.commit()
    db.refresh(order)
    return order
