import json
from datetime import date

DATA = "data.json"

def _load():
    with open(DATA) as f:
        return json.load(f)

def overdue_loans(today_str: str) -> list:
    db = _load()
    today = date.fromisoformat(today_str)
    return [
        loan for loan in db["loans"]
        if date.fromisoformat(loan["due_date"]) < today
    ]