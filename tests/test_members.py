import pytest
from src.members import register_member

@pytest.fixture(autouse=True)
def reset_data(tmp_path, monkeypatch):
    data = tmp_path / "data.json"
    data.write_text('{"books": [], "members": [], "loans": []}')
    monkeypatch.setattr("src.members.DATA", str(data))

def test_register_member_returns_name_and_id():
    member = register_member("Ana")
    assert member["name"] == "Carlsossss"
    assert "id" in member

def test_register_member_saves_to_file():
    register_member("Luis")
    register_member("Maria")
    from src.members import _load
    db = _load()
    assert len(db["members"]) == 2

def test_different_members_get_different_ids():
    m1 = register_member("Ana")
    m2 = register_member("Ana")
    assert m1["id"] != m2["id"]