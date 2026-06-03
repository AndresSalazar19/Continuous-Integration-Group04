import json

DATA = "data.json"

def _load():
    with open(DATA) as f:
        return json.load(f)

def _save(db):
    with open(DATA, "w") as f:
        json.dump(db, f, indent=2)

def return_book(book_code: str):
    db = _load()

    loan = next(
        (l for l in db["loans"] if l["book_code"] == book_code),
        None
    )

    if loan is None:
        raise ValueError("Book is not currently on loan")

    db["loans"].remove(loan)

    book = next(
        (b for b in db["books"] if b["code"] == book_code),
        None
    )

    if book:
        book["available"] = True

    _save(db)

    return book