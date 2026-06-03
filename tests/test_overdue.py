import pytest
from src.overdue import overdue_loans

@pytest.fixture(autouse=True)
def reset_data(tmp_path, monkeypatch):
    data = tmp_path / "data.json"
    data.write_text('{"books": [], "members": [], "loans": []}')
    monkeypatch.setattr("src.overdue.DATA", str(data))

def _add_loan(book_id, member_id, due_date):
    import json
    from src.overdue import DATA
    with open(DATA) as f:
        db = json.load(f)
    db["loans"].append({"book_id": book_id, "member_id": member_id, "due_date": due_date})
    with open(DATA, "w") as f:
        json.dump(db, f)

def test_no_loans_returns_empty():
    result = overdue_loans("2025-06-01")
    assert result == []

def test_past_loan_is_overdue():
    _add_loan("b1", "m1", "2024-01-01")
    result = overdue_loans("2025-06-01")
    assert len(result) == 1
    assert result[0]["book_id"] == "b1"

def test_future_loan_is_not_overdue():
    _add_loan("b1", "m1", "2030-12-31")
    result = overdue_loans("2025-06-01")
    assert result == []

def test_due_today_is_not_overdue():
    _add_loan("b1", "m1", "2025-06-01")
    result = overdue_loans("2025-06-01")
    assert result == []

def test_only_overdue_loans_returned():
    _add_loan("b1", "m1", "2024-01-01")
    _add_loan("b2", "m2", "2030-12-31")
    result = overdue_loans("2025-06-01")
    assert len(result) == 1
    assert result[0]["book_id"] == "b1"