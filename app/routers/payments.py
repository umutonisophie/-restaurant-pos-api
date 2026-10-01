from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.payment import PaymentCreate, PaymentOut
from app.services import payment_service

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/{order_id}", response_model=PaymentOut, status_code=201)
def pay_order(order_id: int, payload: PaymentCreate, db: Session = Depends(get_db)):
    return payment_service.pay_order(db, order_id, payload.method)


@router.get("/{order_id}", response_model=PaymentOut)
def get_payment(order_id: int, db: Session = Depends(get_db)):
    return payment_service.get_payment_or_404(db, order_id)
