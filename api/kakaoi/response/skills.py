from abc import ABCMeta
from pydantic import BaseModel, conlist
from typing import List

from api.kakaoi.response.components.common import (
    QuickReply,
    Thumbnail,
    Button,
    ContextControl,
    ItemCardHead,
    ListCardHeader,
    ListCardItem,
    ItemList,
    ItemListSummary,
    ItemCardImageTitle,
)
from api.kakaoi.response.components.carousel import (
    CarouselHeader,
    CarouselItemCardRow,
    CarouselBasicCardRow,
    CarouselListCardRow,
)


class ABCSkillResponse(BaseModel, metaclass=ABCMeta):
    @property
    def skill_name(self):
        _skill_name = self.__repr_name__()
        return _skill_name[0].lower() + _skill_name[1:]

    def dict(self, *args, **kwargs):
        return {self.skill_name: super().dict()}

    def as_item(self):
        return self.__dict__.copy()


class SimpleText(ABCSkillResponse):
    text: str


class SimpleImage(ABCSkillResponse):
    imageUrl: str
    altText: str = ""


class BasicCard(ABCSkillResponse):
    title: str
    description: str
    thumbnail: Thumbnail
    buttons: conlist(Button, max_items=3) = []
    # profile: Profile
    # social: Social


class CommerceCard(ABCSkillResponse):
    pass


class ListCard(ABCSkillResponse):
    header: ListCardHeader
    items: conlist(ListCardItem, min_items=1, max_items=5)
    buttons: conlist(Button, max_items=2) = []


class ItemCard(ABCSkillResponse):
    thumbnail: Thumbnail = None
    head: ItemCardHead = None
    imageTitle: ItemCardImageTitle = None
    itemList: conlist(ItemList, min_items=1, max_items=10)
    itemListAlignment: str = "left"
    itemListSummary: ItemListSummary = None
    title: str = ""
    description: str = ""
    buttons: List[Button] = []
    buttonLayout: str = "vertical"  # "horizontal"


class Carousel(ABCSkillResponse):
    type: str
    items: List
    header: CarouselHeader = None

    @property
    def skill_name(self):
        return "carousel"


class BasicCardCarousel(Carousel):
    type = "basicCard"
    items: conlist(CarouselBasicCardRow, min_items=1, max_items=10)


class ListCardCarousel(Carousel):
    type = "listCard"
    items: conlist(CarouselListCardRow, min_items=1, max_items=5)


class ItemCardCarousel(Carousel):
    type = "itemCard"
    items: conlist(CarouselItemCardRow, min_items=1, max_items=10)


class SkillTemplate(BaseModel):
    outputs: conlist(ABCSkillResponse, max_items=3)
    quickReplies: conlist(QuickReply, max_items=10) = []


class SkillResponse(BaseModel):
    version: str = "2.0"
    template: SkillTemplate
    context: ContextControl = {}
    data: dict = {}
