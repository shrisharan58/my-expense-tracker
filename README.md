# Smart Expense Tracker API

A REST API built with **FastAPI** for managing personal expenses. The application stores expense data in a local JSON file (`expenses.json`), making it lightweight and easy to set up without requiring a database.

---

## Features

- Add a new expense
- View all expenses
- Retrieve a single expense by ID
- Filter expenses by category
- Calculate total expenses (overall and by category)
- Delete an expense
- Interactive API documentation using Swagger UI
- Automated testing using Pytest

---

## Project Structure

```text
my-expense-tracker/
├── README.md
├── AI_NOTES.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── storage.py
└── tests/
    ├── __init__.py
    └── test_api.py
```

---

## Requirements

- Python 3.10 or later

---

## Installation

### Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Running the Application

### Windows

```bash
python -m uvicorn src.main:app --reload
```

### Linux / macOS

```bash
python3 -m uvicorn src.main:app --reload
```

The server will start at:

```
http://localhost:8000
```

Interactive Swagger documentation:

```
http://localhost:8000/docs
```

Open the above URL in your browser to test all API endpoints directly.

---

## Running the Tests

Execute:

```bash
pytest
```

The test suite uses a temporary JSON file during execution, so your actual `expenses.json` file remains unchanged.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/expenses` | Create a new expense |
| GET | `/expenses` | Retrieve all expenses |
| GET | `/expenses/{id}` | Retrieve an expense by ID |
| GET | `/expenses?category=Food` | Filter expenses by category |
| GET | `/expenses/totals` | Calculate overall and category-wise totals |
| DELETE | `/expenses/{id}` | Delete an expense |

---

## Example Request

### Add an Expense

```bash
curl -X POST http://localhost:8000/expenses \
-H "Content-Type: application/json" \
-d "{\"title\":\"Lunch\",\"amount\":10.50,\"category\":\"Food\",\"date\":\"2026-07-30\"}"
```

---

## Example Response

### Get Expense Totals

```bash
curl http://localhost:8000/expenses/totals
```

Response:

```json
{
  "overall_total": 10.5,
  "by_category": [
    {
      "category": "Food",
      "total": 10.5
    }
  ]
}
```

---

## Design Decisions

- Expense data is stored in a local JSON file instead of a database to keep the project simple and aligned with the assignment requirements.
- FastAPI and Pydantic are used for request validation and automatic API documentation.
- Expense amounts must be positive, and required fields cannot be empty.
- Category filtering is case-insensitive.
- The `/expenses/totals` endpoint is defined before `/expenses/{id}` to prevent routing conflicts.
- This implementation is intended for a single-user environment and is not designed for concurrent writes.

---

## Technologies Used

- Python 3
- FastAPI
- Pydantic
- Uvicorn
- Pytest

---

## Notes

This project was developed as part of a Software Engineering Apprenticeship take-home assignment. All required features were implemented, manually verified using Swagger UI, and tested using Pytest before submission.