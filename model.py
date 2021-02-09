import json


def load_db():
    with open("flashcards_db.json") as f:
        return json.load(f)


def save_db():
    with open("flashcards_db.json", "w") as f:
        return json.dump(db, f)


def load_db_from_file(filepath):
    with open(filepath) as f:
        return json.load(f)


def save_db_to_file(filepath):
    with open(filepath, "w") as f:
        return json.dump(db, f)


db = load_db()
