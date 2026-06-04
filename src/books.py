import json


def register_book(title, code, data_file="data.json"):
    with open(data_file, "r") as f:
        data = json.load(f)

    for book in data["books"]:
        if book["code"] == code:
            raise ValueError("Book code already exists")

    data["books"].append({
        "title": title,
        "code": code
    })

    with open(data_file, "w") as f:
        json.dump(data, f)

    return True