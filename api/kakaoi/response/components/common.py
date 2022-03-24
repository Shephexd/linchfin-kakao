from typing import List
from pydantic import BaseModel


class Link(BaseModel):
    mobile: str = None
    web: str = None
    pc: str = None


class Thumbnail(BaseModel):
    imageUrl: str
    link: Link = None
    fixedRatio: bool = None
    width: int
    height: None


class Button(BaseModel):
    label: str
    action: str
    webLinkUrl: str = None
    messageText: str = None
    phoneNumber: str = None
    blockId: str = None
    extra: dict = {}


class WebLinkButton(Button):
    action: str = "webLInk"
    webLinkUrl: str


class ItemCardImageTitle(BaseModel):
    title: str
    description: str = None
    imageUrl: str = None


class QuickReply(BaseModel):
    label: str
    action: str = "message"
    messageText: str
    blockId: str = None
    extra: dict = {}


class MessageButton(Button):
    action: str = "message"
    messageText: str


class PhoneButton(Button):
    action: str = "phone"


class BlockButton(Button):
    action: str = "block"
    blockId: str


class ShareButton(Button):
    action: str = "share"


class Forwardable(BaseModel):
    flag: bool = True

    def dict(self, *args, **kwargs):
        return {"forwardable": self.flag}


class Profile(BaseModel):
    nickname: str
    imageUrl: str = None


class ListCardHeader(BaseModel):
    title: str


class ListCardItem(BaseModel):
    title: str
    description: str = ""
    imageUrl: str = None
    link: Link = None


class ItemCardHead(BaseModel):
    title: str


class ItemListSummary(BaseModel):
    title: str
    description: str


class ItemListRow(BaseModel):
    title: str
    description: str


class ContextValue(BaseModel):
    name: str
    lifeSpan: int = 10
    params: dict = {}


class ContextControl(BaseModel):
    values: List[ContextValue]
