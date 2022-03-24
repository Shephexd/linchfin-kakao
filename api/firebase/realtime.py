from firebase_admin import db


def get_items(key: str):
    _item, _ = key_store.get(key)
    return _item.get(key, {})


key_store = db.reference()
