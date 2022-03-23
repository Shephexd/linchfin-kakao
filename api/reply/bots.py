from typing import List
from api.kakaoi.request import SkillPayload
from api.kakaoi.response.components.common import (
    ListCardItem,
    ContextControl,
    ContextValue,
)
from api.kakaoi.response.components.carousel import CarouselListCardRow
from api.kakaoi.response.skills import (
    ABCSkillResponse,
    SkillTemplate,
    SkillResponse,
    SimpleText,
    QuickReply,
    ListCardHeader,
    ListCard,
    ItemCardHead,
    ItemCard,
    ItemListRow,
    ListCardCarousel,
)

from api.firebase.realtime import get_items


class MetaBot:
    CONTEXT_LIFESPAN = 10
    ACTION_KEYWORDS = ["홈"]

    def reply(self, payload: SkillPayload) -> SkillResponse:
        response_template = SkillResponse(
            template=SkillTemplate(
                outputs=self.build_replies(payload=payload),
                quickReplies=self.build_quick_replies(payload=payload),
            ),
            context=self.get_context(payload=payload),
            data=self.get_data(payload=payload),
        )
        return response_template

    def build_replies(self, payload) -> List[ABCSkillResponse]:
        return [SimpleText(text=payload.input_text)]

    def build_quick_replies(self, payload: SkillPayload) -> List[QuickReply]:
        quick_replies = [
            QuickReply(label="홈", messageText="홈"),
            QuickReply(label="포트폴리오", messageText="포트폴리오"),
            QuickReply(label="유니버스", messageText="유니버스"),
        ]
        return quick_replies

    def get_context(self, payload: SkillPayload) -> ContextControl:
        return ContextControl(
            values=payload.contexts
            + [ContextValue(name=payload.input_text, lifeSpan=self.CONTEXT_LIFESPAN)]
        )

    def get_data(self, payload: SkillPayload):
        return {"input_text": payload.input_text}

    @classmethod
    def match(cls, input_text: str):
        if input_text in cls.ACTION_KEYWORDS:
            return cls


class PortfolioBot(MetaBot):
    ACTION_KEYWORDS = ["포트폴리오"]

    def build_replies(self, payload) -> List[ABCSkillResponse]:
        _portfolio = get_items(key="portfolio")
        if _portfolio and "weights" in _portfolio:
            return [
                SimpleText(text=f"{_portfolio['base_date']} 기준 포트폴리오입니다."),
                ItemCard(
                    head=ItemCardHead(title=f"{_portfolio['base_date']} 생성"),
                    itemList=[
                        ItemListRow(title=k, description=v)
                        for k, v in _portfolio["weights"].items()
                    ]
                ),
            ]
        return [SimpleText(text="최신 포트폴리오가 등록되지 않았습니다.")]


class UniverseBot(MetaBot):
    ACTION_KEYWORDS = ["유니버스"]

    def build_replies(self, payload) -> List[ABCSkillResponse]:
        print(self.iter_items(payload))
        items = [
            CarouselListCardRow(
                header=ListCardHeader(title=_sector_name),
                items=[ListCardItem(**_asset) for _asset in _assets],
            )
            for _sector_name, _assets in self.iter_items(payload)
        ]

        return [SimpleText(text="포트폴리오 유니버스입니다."), ListCardCarousel(items=items)]

    def iter_items(self, payload: SkillPayload):
        item_context = {
            "배당": [
                dict(title="SDIV", description="저변동성 배당 ETF"),
                dict(title="SPHD", description="글로벌 고배당 ETF"),
                dict(title="DGRW", description="배당 성장 ETF"),
            ],
            "원자재/리츠": [
                dict(title="PDBC", description="원자재 ETF"),
                dict(title="VNQ", description="리츠 ETF"),
            ],
            "성장": [
                dict(title="QQQ", description="나스닥 100 ETF"),
                dict(title="SPY", description="S&P 500 ETF"),
            ],
            "변동성": [
                dict(title="VIXM", description="중기 변동성 ETF"),
            ],
        }
        return item_context.items()
