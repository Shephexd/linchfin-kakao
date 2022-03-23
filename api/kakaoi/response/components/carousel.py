from pydantic import BaseModel, conlist
from api.kakaoi.response.components.common import (
    Thumbnail,
    ListCardHeader,
    ListCardItem,
    Button,
    ItemCardHead,
    ItemCardImageTitle,
    ItemList,
    ItemListSummary,
)


class CarouselHeader(BaseModel):
    title: str
    description: str
    thumbnail: Thumbnail


class CarouselListCardRow(BaseModel):
    header: ListCardHeader
    items: conlist(ListCardItem, max_items=5)
    buttons: conlist(Button, max_items=2) = []


class CarouselBasicCardRow(BaseModel):
    title: str
    description: str
    thumbnail: Thumbnail
    buttons: conlist(Button, max_items=3) = []
    # profile: Profile
    # social: Social


class CarouselItemCardRow(BaseModel):
    thumbnail: Thumbnail = None
    head: ItemCardHead = None
    imageTitle: ItemCardImageTitle = None
    itemList: conlist(ItemList, min_items=1, max_items=5)
    itemListAlignment: str = "left"
    itemListSummary: ItemListSummary = None
    title: str = ""
    description: str = ""
    buttons: conlist(Button, max_items=3) = []
    buttonLayout: str = "vertical"  # "horizontal"
