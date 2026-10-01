from fastapi import FastAPI
from app.core.database import engine, Base
import app.models
from app.routers import tables, menu, orders, payments

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Restaurant POS API")
app.include_router(tables.router)
app.include_router(menu.router)
app.include_router(orders.router)
app.include_router(payments.router)


@app.get("/")
def root():
    return {"message": "Restaurant POS API is running"}
