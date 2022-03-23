from typing import Optional

from fastapi import FastAPI
from api.reply.router import BotRouter
from api.kakaoi.request import SkillPayload
from api.kakaoi.response.skills import SkillResponse, SimpleText, QuickReply

app = FastAPI()
bot_router = BotRouter()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/kakaoi/v1/api/reply")
def reply_kakaoi(payload: SkillPayload):
    return bot_router.reply(payload=payload)


@app.post("/kakaoi/v1/api/reply/echo")
def echo_kakao(payload: SkillPayload):
    reply = bot_router.reply(payload=payload)
    print(payload.dict())
    print(reply.dict())
    return reply.dict()
