from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.order import OrderCreate, OrderOut, OrderItemCreate, OrderItemOut
from app.models.order import OrderStatus
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=201)
def open_order(payload: OrderCreate, db: Session = Depends(get_db)):
    return order_service.open_order(db, payload.table_id)


@router.get("", response_model=List[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return order_service.list_orders(db)


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return order_service.get_order_or_404(db, order_id)


@router.post("/{order_id}/items", response_model=OrderItemOut, status_code=201)
def add_item(order_id: int, payload: OrderItemCreate, db: Session = Depends(get_db)):
    return order_service.add_item(db, order_id, payload.menu_item_id, payload.quantity, payload.notes)


@router.post("/{order_id}/status/{new_status}", response_model=OrderOut)
def advance_status(order_id: int, new_status: OrderStatus, db: Session = Depends(get_db)):
    return order_service.advance_status(db, order_id, new_status)


@router.get("/{order_id}/total")
def get_total(order_id: int, db: Session = Depends(get_db)):
    order = order_service.get_order_or_404(db, order_id)
    return {"order_id": order_id, "total": order_service.calculate_total(order)}