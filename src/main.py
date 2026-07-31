"""Smart Expense Tracker API.

Endpoints:
  POST   /expenses              add an expense
  GET    /expenses              list expenses (optional ?category= filter)
  GET    /expenses/{id}         get a single expense
  DELETE /expenses/{id}         delete an expense
  GET    /expenses/totals       overall total + totals by category
"""
import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .models import Expense, ExpenseCreate, TotalsResponse, CategoryTotal
from .storage import ExpenseStore

app = FastAPI(
    title="Smart Expense Tracker API",
    description="A small REST API for tracking personal expenses.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data file location can be overridden (tests point this at a temp file).
DATA_FILE = os.environ.get("EXPENSE_DATA_FILE", "expenses.json")
store = ExpenseStore(DATA_FILE)


@app.get("/")
def root():
    return {"status": "ok", "service": "expense-tracker-api"}


@app.post("/expenses", response_model=Expense, status_code=201)
def add_expense(payload: ExpenseCreate):
    return store.add(payload)


@app.get("/expenses", response_model=list[Expense])
def list_expenses(category: str | None = Query(default=None, description="Filter by category")):
    return store.list_all(category=category)


@app.get("/expenses/totals", response_model=TotalsResponse)
def get_totals():
    overall, by_cat = store.totals()
    return TotalsResponse(
        overall_total=overall,
        by_category=[CategoryTotal(category=c, total=t) for c, t in by_cat.items()],
    )


@app.get("/expenses/{expense_id}", response_model=Expense)
def get_expense(expense_id: int):
    expense = store.get(expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail=f"Expense {expense_id} not found")
    return expense


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    deleted = store.delete(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Expense {expense_id} not found")
    return None
