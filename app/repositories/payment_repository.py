from typing import Optional
from sqlalchemy.orm import Session, selectinload
from app.models.payment import Payment, PaymentMethod


def create_payment(db: Session, order_id: int, amount: float, method: PaymentMethod) -> Payment:
    payment = Payment(order_id=order_id, amount=amount, method=method)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_payment(db: Session, order_id: int) -> Optional[Payment]:
    return db.query(Payment).options(
        selectinload(Payment.order),
    ).filter(Payment.order_id == order_id).first()