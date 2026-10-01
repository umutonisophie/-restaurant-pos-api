from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.table import TableCreate, TableOut
from app.models.table import TableStatus
from app.services import table_service

router = APIRouter(prefix="/tables", tags=["tables"])


@router.post("", response_model=TableOut, status_code=201)
def create_table(payload: TableCreate, db: Session = Depends(get_db)):
    return table_service.create_table(db, payload.number, payload.seats)


@router.get("", response_model=List[TableOut])
def list_tables(db: Session = Depends(get_db)):
    return table_service.list_tables(db)


@router.get("/{table_id}", response_model=TableOut)
def get_table(table_id: int, db: Session = Depends(get_db)):
    return table_service.get_table_or_404(db, table_id)
