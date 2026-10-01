# restaurant_pos

A point-of-sale API for a restaurant, built with FastAPI and SQLAlchemy, layered
into routers, services, schemas and models.

The structure is the point of the project: HTTP concerns stay in the routers,
business rules stay in the services, and the services never see a raw SQL
session's shape. Each layer can be tested without the ones above it.

## Domain

| Model | Purpose |
|---|---|
| `Table` | Physical table, its capacity and whether it is occupied |
| `MenuItem` | What can be ordered, with category and price |
| `Order` | A ticket for one table, tracking its status and total |
| `Payment` | A payment against an order, with method and amount |

Services: `table_service`, `menu_service`, `order_service`, `payment_service`.

## Status flow

An order moves through a fixed lifecycle, and the service layer is what
enforces it:

```
placed -> preparing -> served -> paid
```

Rejecting an invalid transition (marking a paid order as served again, for
example) belongs in the service rather than the route, because it is a domain
rule and should hold however the request arrived.

## Running

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Interactive docs at <http://127.0.0.1:8000/docs>.

## Tests

```bash
pytest tests
```

10 tests covering the workflow end to end: seating a party, adding items,
transitioning an order, and settling the bill.

Run them from this directory. The project uses a top-level `app` package, so
running pytest from a parent directory can shadow it with an unrelated
`app.py` and fail to import.

## Project layout

```
app/
  main.py         application factory and router registration
  core/           configuration and database setup
  models/         SQLAlchemy ORM models
  schemas/        Pydantic request/response validation
  services/       business rules
  repositories/   data access
  routers/        HTTP endpoints
tests/            workflow tests
```

## Notes

- The database is SQLite for local development. `requirements.txt` includes the
  PostgreSQL driver for a deployed environment.
- No authentication yet. The endpoint surface is open, which is fine for a local
  tool and would need role-scoped access before any real deployment, since orders
  and payments are not public data.
