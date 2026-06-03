import json
import uuid

DATA = "data.json"

def _load():
    with open(DATA) as f:
        return json.load(f)

def _save(db):
    with open(DATA, "w") as f:
        json.dump(db, f, indent=2)

def register_member(name: str) -> dict:
    db = _load()
    member = {"id": str(uuid.uuid4()), "name": name}
    db["members"].append(member)
    _save(db)
    return member