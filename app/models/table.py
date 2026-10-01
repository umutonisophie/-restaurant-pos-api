import enum
from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base


class TableStatus(str, enum.Enum):
    free = "free"
    occupied = "occupied"


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, nullable=False)
    seats = Column(Integer, nullable=False, default=2)
    status = Column(Enum(TableStatus), nullable=False, default=TableStatus.free)

    orders = relationship("Order", back_populates="table")