from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories import order_repository, menu_repository
from app.services import table_service
from app.models.order import Order, OrderStatus
from app.models.table import TableStatus

ALLOWED_TRANSITIONS = {
    OrderStatus.open: {OrderStatus.in_progress, OrderStatus.cancelled},
    OrderStatus.in_progress: {OrderStatus.served, OrderStatus.cancelled},
    OrderStatus.served: {OrderStatus.paid},
    OrderStatus.paid: set(),
    OrderStatus.cancelled: set(),
}


def open_order(db: Session, table_id: int) -> Order:
    table = table_service.get_table_or_404(db, table_id)
    if table.status == TableStatus.occupied:
        raise HTTPException(400, "Table is already occupied by an open order")

    order = order_repository.create_order(db, table_id)
    table_service.set_status(db, table, TableStatus.occupied)
    return order


def get_order_or_404(db: Session, order_id: int) -> Order:
    order = order_repository.get_order(db, order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    return order


def list_orders(db: Session):
    return order_repository.list_orders(db)


def add_item(db: Session, order_id: int, menu_item_id: int, quantity: int, notes: Optional[str]):
    order = get_order_or_404(db, order_id)
    if order.status in (OrderStatus.paid, OrderStatus.cancelled):
        raise HTTPException(400, f"Cannot add items to an order that is already {order.status.value}")

    menu_item = menu_repository.get_menu_item(db, menu_item_id)
    if not menu_item:
        raise HTTPException(404, "Menu item not found")
    if not menu_item.available:
        raise HTTPException(400, f"'{menu_item.name}' is currently unavailable")

    return order_repository.add_item(db, order_id, menu_item_id, quantity, notes, price=menu_item.price)


def advance_status(db: Session, order_id: int, new_status: OrderStatus) -> Order:
    order = get_order_or_404(db, order_id)
    allowed = ALLOWED_TRANSITIONS.get(order.status, set())
    if new_status not in allowed:
        raise HTTPException(400, f"Cannot move order from '{order.status.value}' to '{new_status.value}'")
    order = order_repository.set_status(db, order, new_status)

    if new_status == OrderStatus.cancelled:
        table_service.set_status(db, order.table, TableStatus.free)

    return order


def calculate_total(order: Order) -> float:
    return sum(item.price_at_order_time * item.quantity for item in order.items)