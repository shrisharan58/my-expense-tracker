"""Simple JSON-file-backed storage for expenses.

Not meant to be highly concurrent or production-grade - this is
intentionally simple per the assignment brief (no database required).
"""
import json
import threading
from pathlib import Path
from datetime import date
from typing import Optional

from .models import Expense, ExpenseCreate


class ExpenseStore:
    def __init__(self, file_path: str = "expenses.json"):
        self.file_path = Path(file_path)
        self._lock = threading.Lock()
        self._expenses: dict[int, Expense] = {}
        self._next_id = 1
        self._load()

    # ---------- persistence ----------
    def _load(self) -> None:
        if not self.file_path.exists():
            return
        try:
            raw = json.loads(self.file_path.read_text())
        except (json.JSONDecodeError, OSError):
            return
        for item in raw:
            exp = Expense(**item)
            self._expenses[exp.id] = exp
        if self._expenses:
            self._next_id = max(self._expenses.keys()) + 1

    def _save(self) -> None:
        data = [json.loads(e.model_dump_json()) for e in self._expenses.values()]
        self.file_path.write_text(json.dumps(data, indent=2, default=str))

    # ---------- CRUD ----------
    def add(self, payload: ExpenseCreate) -> Expense:
        with self._lock:
            expense = Expense(id=self._next_id, **payload.model_dump())
            self._expenses[expense.id] = expense
            self._next_id += 1
            self._save()
            return expense

    def list_all(self, category: Optional[str] = None) -> list[Expense]:
        items = list(self._expenses.values())
        if category:
            items = [e for e in items if e.category.lower() == category.lower()]
        return sorted(items, key=lambda e: e.date)

    def get(self, expense_id: int) -> Optional[Expense]:
        return self._expenses.get(expense_id)

    def delete(self, expense_id: int) -> bool:
        with self._lock:
            if expense_id not in self._expenses:
                return False
            del self._expenses[expense_id]
            self._save()
            return True

    def totals(self) -> tuple[float, dict[str, float]]:
        overall = 0.0
        by_category: dict[str, float] = {}
        for e in self._expenses.values():
            overall += e.amount
            by_category[e.category] = by_category.get(e.category, 0.0) + e.amount
        return round(overall, 2), {k: round(v, 2) for k, v in by_category.items()}

    def clear(self) -> None:
        """Used by tests to reset state between runs."""
        with self._lock:
            self._expenses.clear()
            self._next_id = 1
            self._save()
