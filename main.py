from fastapi import FastAPI
from api.reply.router import BotRouter
from api.kakaoi.request import SkillPayload
from api.firebase.realtime import key_store


app = FastAPI()
bot_router = BotRouter()


@app.post("/api/v1/kakaoi/reply")
def reply_kakaoi(payload: SkillPayload):
    return bot_router.reply(payload=payload)


@app.post("/api/v1/kakaoi/reply/echo")
def echo_kakao(payload: SkillPayload):
    reply = bot_router.reply(payload=payload)
    print(payload.dict())
    print(reply.dict())
    return reply.dict()


@app.get("/api/v1/firebase/items/")
def get_key():
    dic = key_store.get("")
    return list(dic.keys())


@app.get("/api/v1/firebase/items/{item_id}")
def get_key(item_id: str):
    dic, _ = key_store.get(item_id)
    return dic[item_id]


@app.post("/api/v1/firebase/items")
def update_key(item_id: str, payload: dict):
    key_store.update({item_id: payload})
    return payload
