import pytest
from src.returns import return_book

@pytest.fixture(autouse=True)
def reset_data(tmp_path, monkeypatch):
    data = tmp_path / "data.json"

    data.write_text("""
    {
      "books": [
        {
          "code": "B001",
          "title": "Clean Code",
          "available": false
        }
      ],
      "members": [],
      "loans": [
        {
          "book_code": "B001",
          "member_id": "M001"
        }
      ]
    }
    """)

    monkeypatch.setattr("src.returns.DATA", str(data))

def test_return_book_marks_book_available():
    return_book("B001")

    from src.returns import _load
    db = _load()

    assert db["books"][0]["available"] is True

def test_return_book_removes_loan():
    return_book("B001")

    from src.returns import _load
    db = _load()

    assert len(db["loans"]) == 0

def test_returning_non_loaned_book_raises_error():
    with pytest.raises(ValueError):
        return_book("B999")