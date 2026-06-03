# src/library.py

def list_member_loans(member_id: str, data: dict) -> list:
    """
    Returns the active loans of a member.
    Throws ValueError if the member does not exist.
    """
    member_exists = any(m["id"] == member_id for m in data["members"])
    if not member_exists:
        raise ValueError(f"Member '{member_id}' not found.")

    loans = [
        loan for loan in data["loans"]
        if loan["member_id"] == member_id
    ]
    return loans