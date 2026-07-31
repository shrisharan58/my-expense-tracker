"""Pydantic models for the Expense Tracker API."""
from datetime import date
from pydantic import BaseModel, Field, field_validator


class ExpenseCreate(BaseModel):
    """Payload for creating a new expense. id is server-assigned."""
    title: str = Field(..., min_length=1, max_length=200)
    amount: float = Field(..., gt=0, description="Must be a positive number")
    category: str = Field(..., min_length=1, max_length=100)
    date: date

    @field_validator("title", "category")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("must not be blank")
        return v.strip()


class Expense(ExpenseCreate):
    """Full expense record as stored/returned by the API."""
    id: int


class CategoryTotal(BaseModel):
    category: str
    total: float


class TotalsResponse(BaseModel):
    overall_total: float
    by_category: list[CategoryTotal]
