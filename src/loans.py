import json

DATA = "data.json"

MAX_BOOKS_PER_MEMBER = 3


class LoanError(Exception):
    """Raised when a loan request violates a library rule."""


def _load():
    with open(DATA) as f:
        return json.load(f)


def _save(db):
    with open(DATA, "w") as f:
        json.dump(db, f, indent=2)


def _book_exists(db, book_code):
    return any(book["code"] == book_code for book in db["books"])


def _member_exists(db, member_id):
    return any(member["id"] == member_id for member in db["members"])


def is_on_loan(db, book_code):
    return any(loan["book_code"] == book_code for loan in db["loans"])


def member_loan_count(db, member_id):
    return sum(1 for loan in db["loans"] if loan["member_id"] == member_id)


def loan_book(book_code: str, member_id: str, due_date: str) -> dict:
    db = _load()
    if not _book_exists(db, book_code):
        raise LoanError(f"No existe un libro con el codigo '{book_code}'.")
    if not _member_exists(db, member_id):
        raise LoanError(f"No existe un miembro con el identificador '{member_id}'.")
    if is_on_loan(db, book_code):
        raise LoanError(
            f"El libro '{book_code}' ya esta prestado; no puede prestarse de nuevo."
        )
    if member_loan_count(db, member_id) >= MAX_BOOKS_PER_MEMBER:
        raise LoanError(
            f"El miembro '{member_id}' ya tiene {MAX_BOOKS_PER_MEMBER} libros prestados "
            f"(es el maximo permitido)."
        )

    loan = {"book_code": book_code, "member_id": member_id, "due_date": due_date}
    db["loans"].append(loan)
    _save(db)
    return loan