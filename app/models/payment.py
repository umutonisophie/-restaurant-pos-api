import enum
from sqlalchemy import Column, Integer, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base, utcnow


class PaymentMethod(str, enum.Enum):
    cash = "cash"
    card = "card"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(Enum(PaymentMethod), nullable=False)
    paid_at = Column(DateTime, default=utcnow)

    order = relationship("Order", back_populates="payment")