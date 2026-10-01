from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, computed_field
from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = 1
    notes: Optional[str] = None


class OrderCreate(BaseModel):
    table_id: int


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    menu_item_id: int
    quantity: int
    notes: Optional[str]
    price_at_order_time: float

    @computed_field
    @property
    def total_price(self) -> float:
        return self.price_at_order_time * self.quantity


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    table_id: int
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemOut] = []

    @computed_field
    @property
    def total(self) -> float:
        return sum(item.total_price for item in self.items)
