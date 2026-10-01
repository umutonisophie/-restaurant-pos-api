from pydantic import BaseModel, ConfigDict
from app.models.table import TableStatus


class TableCreate(BaseModel):
    number: int
    seats: int = 2


class TableOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: int
    seats: int
    status: TableStatus