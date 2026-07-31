"""Tests for the Expense Tracker API.

Run with: pytest
Each test run uses a fresh temp JSON file so tests don't interfere
with each other or with any real expenses.json on disk.
"""
import os
import tempfile
import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    # Point storage at a throwaway temp file BEFORE importing the app,
    # since the app module creates its ExpenseStore at import time.
    tmp_dir = tempfile.mkdtemp()
    data_file = os.path.join(tmp_dir, "expenses.json")
    os.environ["EXPENSE_DATA_FILE"] = data_file

    from src.main import app, store
    store.file_path = __import__("pathlib").Path(data_file)
    store.clear()

    with TestClient(app) as c:
        yield c

    store.clear()


def make_expense(**overrides):
    payload = {
        "title": "Coffee",
        "amount": 4.5,
        "category": "Food",
        "date": "2026-07-01",
    }
    payload.update(overrides)
    return payload


def test_root(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_add_expense(client):
    resp = client.post("/expenses", json=make_expense())
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Coffee"
    assert body["amount"] == 4.5
    assert body["id"] == 1


def test_add_expense_rejects_non_positive_amount(client):
    resp = client.post("/expenses", json=make_expense(amount=0))
    assert resp.status_code == 422

    resp2 = client.post("/expenses", json=make_expense(amount=-5))
    assert resp2.status_code == 422


def test_add_expense_rejects_blank_title(client):
    resp = client.post("/expenses", json=make_expense(title="   "))
    assert resp.status_code == 422


def test_list_expenses_empty(client):
    resp = client.get("/expenses")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_expenses_returns_added_items(client):
    client.post("/expenses", json=make_expense(title="Coffee"))
    client.post("/expenses", json=make_expense(title="Bus ticket", category="Transport", amount=2.0))

    resp = client.get("/expenses")
    assert resp.status_code == 200
    titles = {e["title"] for e in resp.json()}
    assert titles == {"Coffee", "Bus ticket"}


def test_filter_by_category(client):
    client.post("/expenses", json=make_expense(title="Coffee", category="Food"))
    client.post("/expenses", json=make_expense(title="Bus ticket", category="Transport", amount=2.0))
    client.post("/expenses", json=make_expense(title="Pizza", category="food", amount=12.0))  # case-insensitive match

    resp = client.get("/expenses", params={"category": "Food"})
    assert resp.status_code == 200
    titles = {e["title"] for e in resp.json()}
    assert titles == {"Coffee", "Pizza"}


def test_get_single_expense(client):
    created = client.post("/expenses", json=make_expense()).json()
    resp = client.get(f"/expenses/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Coffee"


def test_get_single_expense_not_found(client):
    resp = client.get("/expenses/999")
    assert resp.status_code == 404


def test_totals_overall_and_by_category(client):
    client.post("/expenses", json=make_expense(title="Coffee", category="Food", amount=4.5))
    client.post("/expenses", json=make_expense(title="Pizza", category="Food", amount=12.0))
    client.post("/expenses", json=make_expense(title="Bus ticket", category="Transport", amount=2.0))

    resp = client.get("/expenses/totals")
    assert resp.status_code == 200
    body = resp.json()
    assert body["overall_total"] == 18.5

    by_cat = {c["category"]: c["total"] for c in body["by_category"]}
    assert by_cat["Food"] == 16.5
    assert by_cat["Transport"] == 2.0


def test_delete_expense(client):
    created = client.post("/expenses", json=make_expense()).json()
    expense_id = created["id"]

    resp = client.delete(f"/expenses/{expense_id}")
    assert resp.status_code == 204

    resp2 = client.get(f"/expenses/{expense_id}")
    assert resp2.status_code == 404


def test_delete_nonexistent_expense_returns_404(client):
    resp = client.delete("/expenses/999")
    assert resp.status_code == 404


def test_data_persists_to_json_file(client):
    client.post("/expenses", json=make_expense())
    data_file = os.environ["EXPENSE_DATA_FILE"]
    assert os.path.exists(data_file)

    import json
    with open(data_file) as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]["title"] == "Coffee"
