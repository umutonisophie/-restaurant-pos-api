from typing import Optional, List
from sqlalchemy.orm import Session, selectinload
from app.models.table import Table, TableStatus


def create_table(db: Session, number: int, seats: int) -> Table:
    table = Table(number=number, seats=seats)
    db.add(table)
    db.commit()
    db.refresh(table)
    return table


def get_table(db: Session, table_id: int) -> Optional[Table]:
    return db.query(Table).filter(Table.id == table_id).first()


def list_tables(db: Session) -> List[Table]:
    return db.query(Table).options(selectinload(Table.orders)).all()


def set_status(db: Session, table: Table, status: TableStatus) -> Table:
    table.status = status
    db.commit()
    db.refresh(table)
    return table