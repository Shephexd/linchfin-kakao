from typing import List
from api.kakaoi.request import SkillPayload
from api.kakaoi.response.components.common import (
    ListCardItem,
    ContextControl,
    ContextValue,
    MessageButton,
    WebLinkButton,
)
from api.kakaoi.response.components.carousel import CarouselListCardRow
from api.kakaoi.response.skills import (
    ABCSkillResponse,
    SkillTemplate,
    SkillResponse,
    SimpleText,
    QuickReply,
    ListCardHeader,
    Thumbnail,
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
            values=payload.get_next_contexts()
            + [
                ContextValue(
                    name="payload",
                    lifeSpan=self.CONTEXT_LIFESPAN,
                    params={"input_text": payload.input_text},
                )
            ]
        )

    def get_data(self, payload: SkillPayload):
        return {}

    @classmethod
    def match(cls, input_text: str):
        if input_text in cls.ACTION_KEYWORDS:
            return cls


class PortfolioBot(MetaBot):
    ACTION_KEYWORDS = ["포트폴리오"]
    IMAGE_URL = "https://s3.us-west-2.amazonaws.com/secure.notion-static.com/5a7a3aaf-688b-4c27-ad79-08086817e05a/Portfolio.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220324%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220324T075834Z&X-Amz-Expires=86400&X-Amz-Signature=2d8e7198ffa41c976c08a90acf651165df6a7711cabd6e0b22cf563cd7d5c772&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Portfolio.png%22&x-id=GetObject"

    def build_replies(self, payload) -> List[ABCSkillResponse]:
        _portfolio = get_items(key="portfolio")
        if _portfolio and "weights" in _portfolio:
            return [
                SimpleText(text=f"{_portfolio['base_date']} 기준 포트폴리오입니다."),
                ItemCard(
                    thumbnail=self.get_thumbnail(),
                    itemList=[
                        ItemListRow(title=k, description=f"{round(float(v) * 100, 3)}%")
                        for k, v in _portfolio["weights"].items()
                    ],
                    description=f"{_portfolio['base_date']} 기준",
                    buttons=[
                        MessageButton(label="수량 계산", messageText="포트폴리오 수량 계산"),
                        WebLinkButton(label="상세 보기", webLinkUrl=self.IMAGE_URL),
                    ],
                ),
            ]
        return [SimpleText(text="최신 포트폴리오가 등록되지 않았습니다.")]

    def get_thumbnail(self) -> Thumbnail:
        return Thumbnail(
            imageUrl=self.IMAGE_URL, width=800, height=400, fixedRatio=False
        )


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
