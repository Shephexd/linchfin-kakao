import firebase_admin
from firebase_admin import credentials
from config import FIREBASE


if "CREDENTIAL" in FIREBASE:
    credential = credentials.Certificate(FIREBASE["CREDENTIAL"])
    app = firebase_admin.initialize_app(
        credential, {"databaseURL": FIREBASE["REALTIME_DB"]}
    )
