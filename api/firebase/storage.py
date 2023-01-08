from firebase_admin import storage
from config import FIREBASE


def get_file(file_name: str):
    _blob = bucket.blob(file_name)
    if _blob.exists():
        return _blob.download_as_bytes()
    raise FileNotFoundError(f"Can't find file in bucket")


bucket = storage.bucket(FIREBASE["STORAGE_BUCKET"])
