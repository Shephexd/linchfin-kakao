from pydantic import BaseModel
from typing import List
from api.kakaoi.response.components.common import ContextValue


class SkillPayloadIntentField(BaseModel):
    id: str
    name: str


class SkillPayloadUserRequestField(BaseModel):
    timezone: str
    params: dict
    block: dict
    utterance: str
    lang: str = None
    user: dict


class SkillPayloadBotField(BaseModel):
    id: str
    name: str


class SkillPayloadActionField(BaseModel):
    name: str
    clientExtra: dict = None
    params: dict
    id: str
    detailParams: dict


class SkillPayload(BaseModel):
    intent: SkillPayloadIntentField
    userRequest: SkillPayloadUserRequestField
    bot: SkillPayloadBotField
    action: SkillPayloadActionField
    contexts: List[ContextValue] = []

    @property
    def input_text(self) -> str:
        return self.userRequest.utterance

    def get_next_contexts(self):
        return [
            ContextValue(name=c.name, lifeSpan=c.lifeSpan - 1, params=c.params)
            for c in self.contexts
            if c.lifeSpan - 1 > 0
        ]
