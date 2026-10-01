from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.payment import PaymentMethod


class PaymentCreate(BaseModel):
    method: PaymentMethod


class PaymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_id: int
    amount: float
    method: PaymentMethod
    paid_at: datetime