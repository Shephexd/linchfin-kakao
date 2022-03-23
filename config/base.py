import logging
import os
import json
import base64


def encode_credential(credential: dict, encoding="utf-8") -> bytes:
    _dumped = json.dumps(credential.copy())
    return base64.b64encode(_dumped.encode(encoding=encoding))


def decode_credential(encoded: str or bytes, encoding="utf-8") -> dict:
    if isinstance(encoded, bytes):
        encoded = encoded.decode(encoding=encoding)
    decoded = base64.b64decode(encoded)
    return json.loads(decoded)


FIREBASE = {
    "REALTIME_DB": os.getenv("FIREBASE_REALTIME_DB", ""),
}
try:
    FIREBASE["CREDENTIAL"] = decode_credential(os.getenv("FIREBASE_CREDENTIAL", ""))
except json.JSONDecodeError as e:
    logging.warning("FIREBASE_CREDENTIAL NOT SET")
