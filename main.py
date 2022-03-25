import io
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from api.reply.router import BotRouter
from api.kakaoi.request import SkillPayload

from api.firebase import realtime, storage


app = FastAPI()
bot_router = BotRouter()


@app.post("/api/v1/kakaoi/reply")
def reply_kakaoi(payload: SkillPayload):
    reply = bot_router.reply(payload=payload)
    return reply.dict(exclude_none=True)


@app.post("/api/v1/kakaoi/reply/echo")
def echo_kakao(payload: SkillPayload):
    print("INPUT", payload.dict(exclude_none=True))
    reply = bot_router.reply(payload=payload)
    print("OUTPUT", reply.dict(exclude_none=True))
    return reply.dict(exclude_none=True)


@app.get("/api/v1/firebase/items/")
def get_key():
    dic = realtime.key_store.get("")
    return list(dic.keys())


@app.get("/api/v1/firebase/items/{item_id}")
def get_key(item_id: str):
    dic, _ = realtime.key_store.get(item_id)
    return dic[item_id]


@app.post("/api/v1/firebase/items")
def update_key(item_id: str, payload: dict):
    realtime.key_store.update({item_id: payload})
    return payload


@app.get("/api/v1/backtest/result")
def get_file():
    b = io.BytesIO(storage.get_file(file_name="backtest/backtest.png"))
    return StreamingResponse(b, media_type="image/png")
