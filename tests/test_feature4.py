import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from library import list_member_loans


def test_member_with_two_loans():
    data = {
        "members": [{"id": "m1", "name": "Ana"}],
        "books": [
            {"id": "b1", "title": "Clean Code"},
            {"id": "b2", "title": "The Pragmatic Programmer"}
        ],
        "loans": [
            {"member_id": "m1", "book_id": "b1"},
            {"member_id": "m1", "book_id": "b2"},
        ]
    }
    result = list_member_loans("m1", data)
    assert len(result) == 2


def test_member_with_no_loans():
    data = {
        "members": [{"id": "m1", "name": "Ana"}],
        "books": [],
        "loans": []
    }
    result = list_member_loans("m1", data)
    assert result == []


def test_member_not_found():
    data = {"members": [], "books": [], "loans": []}
    try:
        list_member_loans("inexistente", data)
        assert False, "Debió lanzar ValueError"
    except ValueError:
        pass