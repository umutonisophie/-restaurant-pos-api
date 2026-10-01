from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories import payment_repository
from app.services import order_service, table_service
from app.models.order import OrderStatus
from app.models.table import TableStatus
from app.models.payment import PaymentMethod, Payment


def pay_order(db: Session, order_id: int, method: PaymentMethod) -> Payment:
    order = order_service.get_order_or_404(db, order_id)

    if order.status != OrderStatus.served:
        raise HTTPException(400, f"Order must be 'served' before payment (currently '{order.status.value}')")
    if not order.items:
        raise HTTPException(400, "Cannot pay for an order with no items")

    amount = order_service.calculate_total(order)
    payment = payment_repository.create_payment(db, order_id, amount, method)

    order_service.advance_status(db, order_id, OrderStatus.paid)
    table_service.set_status(db, order.table, TableStatus.free)

    return payment


def get_payment_or_404(db: Session, order_id: int) -> Payment:
    payment = payment_repository.get_payment(db, order_id)
    if not payment:
        raise HTTPException(404, "Payment not found for this order")
    return payment