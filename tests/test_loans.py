import json
import pytest

from src.loans import (
    MAX_BOOKS_PER_MEMBER,
    LoanError,
    _load,
    is_on_loan,
    loan_book,
    member_loan_count,
)


@pytest.fixture(autouse=True)
def seed_data(tmp_path, monkeypatch):
    data = tmp_path / "data.json"
    db = {
        "books": [
            {"code": "B001", "title": "Cien anos de soledad"},
            {"code": "B002", "title": "Rayuela"},
            {"code": "B003", "title": "Ficciones"},
            {"code": "B004", "title": "Pedro Paramo"},
        ],
        "members": [
            {"id": "M001", "name": "Ana"},
            {"id": "M002", "name": "Luis"},
        ],
        "loans": [],
    }
    data.write_text(json.dumps(db))
    monkeypatch.setattr("src.loans.DATA", str(data))


def test_loan_book_persists_the_loan():
    loan = loan_book("B001", "M001", "2026-06-30")
    assert loan == {"book_code": "B001", "member_id": "M001", "due_date": "2026-06-30"}
    assert _load()["loans"] == [loan]


def test_unknown_book_is_rejected():
    with pytest.raises(LoanError):
        loan_book("NO-EXISTE", "M001", "2026-06-30")
    assert _load()["loans"] == []


def test_unknown_member_is_rejected():
    with pytest.raises(LoanError):
        loan_book("B001", "NO-EXISTE", "2026-06-30")
    assert _load()["loans"] == []


def test_book_already_on_loan_cannot_be_loaned_again():
    loan_book("B001", "M001", "2026-06-30")
    with pytest.raises(LoanError):
        loan_book("B001", "M002", "2026-07-15")
    db = _load()
    assert sum(1 for loan in db["loans"] if loan["book_code"] == "B001") == 1


def test_member_cannot_exceed_the_limit():
    loan_book("B001", "M001", "2026-06-30")
    loan_book("B002", "M001", "2026-06-30")
    loan_book("B003", "M001", "2026-06-30")
    assert member_loan_count(_load(), "M001") == MAX_BOOKS_PER_MEMBER
    with pytest.raises(LoanError):
        loan_book("B004", "M001", "2026-06-30")


def test_two_members_can_each_borrow_a_book():
    loan_book("B001", "M001", "2026-06-30")
    loan_book("B002", "M002", "2026-06-30")
    assert len(_load()["loans"]) == 2
    assert is_on_loan(_load(), "B001")