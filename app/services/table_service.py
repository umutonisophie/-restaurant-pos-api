from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import table_repository
from app.models.table import Table, TableStatus


def create_table(db: Session, number: int, seats: int):
    return table_repository.create_table(db, number, seats)


def list_tables(db: Session):
    return table_repository.list_tables(db)


def get_table_or_404(db: Session, table_id: int):
    table = table_repository.get_table(db, table_id)
    if not table:
        raise HTTPException(404, "Table not found")
    return table


def set_status(db: Session, table: Table, status: TableStatus):
    return table_repository.set_status(db, table, status)