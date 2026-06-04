import json
import tempfile

from src.books import register_book


def test_register_book():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        json.dump(
            {"books": [], "members": [], "loans": []},
            f
        )
        filename = f.name

    register_book("Clean Code", "B001", filename)

    with open(filename, "r") as f:
        data = json.load(f)

    assert len(data["books"]) == 1
    assert data["books"][0]["title"] == "Clean Code"
    assert data["books"][0]["code"] == "B001"


def test_duplicate_code():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        json.dump(
            {
                "books": [
                    {"title": "Clean Code", "code": "B001"}
                ],
                "members": [],
                "loans": []
            },
            f
        )
        filename = f.name

    try:
        register_book("Python Crash Course", "B001", filename)
        assert False
    except ValueError:
        assert True