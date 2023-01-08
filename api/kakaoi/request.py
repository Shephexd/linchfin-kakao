from pydantic import BaseModel
from typing import List, Optional, Union, Dict
from api.kakaoi.response.components.common import ContextValue


class IntentField(BaseModel):
    class IntentExtraField(BaseModel):
        class IntentKnowledgeField(BaseModel):
            answer: str
            question: str
            categories: List[str]
            landingUrl: str
            imageUrl: str

        knowledges: List[IntentKnowledgeField] = []

    id: str
    name: str
    extra: Union[dict, IntentExtraField] = {}


class UserRequestField(BaseModel):
    class UserRequestBlockField(BaseModel):
        id: str
        name: str

    class UserRequestUserField(BaseModel):
        class UserRequestUserPropertiesField(BaseModel):
            plusfriendUserKey: Optional[str]
            appUserId: Optional[str]
            isFriend: bool = None

        id: str
        type: str
        properties: UserRequestUserPropertiesField

    timezone: str
    block: UserRequestBlockField
    utterance: str
    lang: Optional[str] = None
    user: UserRequestUserField


class BotField(BaseModel):
    id: str
    name: str


class ActionField(BaseModel):
    id: str
    name: str
    params: Dict[str, str]
    detailParams: Dict[str, dict]
    clientExtra: Optional[dict]


class SkillPayload(BaseModel):

    intent: IntentField
    userRequest: UserRequestField
    bot: BotField
    action: ActionField
    contexts: List[ContextValue] = []

    @property
    def input_text(self) -> str:
        return self.userRequest.utterance

    @property
    def block_name(self) -> str:
        return self.userRequest.block["name"]

    def get_next_contexts(self):
        return [
            ContextValue(name=c.name, lifeSpan=c.lifeSpan - 1, params=c.params)
            for c in self.contexts
            if c.lifeSpan - 1 > 0
        ]
