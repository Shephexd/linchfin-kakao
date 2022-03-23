from pydantic import BaseModel


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
    contexts: list = []

    @property
    def input_text(self) -> str:
        return self.userRequest.utterance
