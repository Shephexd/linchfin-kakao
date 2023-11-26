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
from actions.gpt.agent import ask_gpt_reply


def divide_long_text(text: str) -> List[str]:
    text_tokens = text.split("\n")
    token_size = len(text_tokens)
    response_block_size = (len(text) // 500) + 1

    response_texts = []
    start, end = 0, -1
    for i in range(response_block_size):
        end = (token_size * (i + 1)) // response_block_size
        response_texts.append(
            "\n".join(text_tokens[start:end])
        )
        start += end
    return response_texts


class MetaBot:
    bots = {}
    CONTEXT_LIFESPAN = 10
    ACTION_KEYWORDS = ["홈"]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.bots[cls] = []

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
        input_history = [c.params["input_text"] for c in payload.contexts
                         if c.name == "payload" and "input_text" in c.params]
        gpt_response = ask_gpt_reply(input_msg=payload.input_text, input_history=input_history)
        if len(gpt_response) < 500:
            return [SimpleText(text=gpt_response)]
        else:
            divided_texts = divide_long_text(text=gpt_response)
            return [SimpleText(text=text) for text in divided_texts]

    def build_quick_replies(self, payload: SkillPayload) -> List[QuickReply]:
        quick_replies = [
            QuickReply(label="홈", messageText="홈"),
            QuickReply(label="포트폴리오", messageText="포트폴리오"),
            QuickReply(label="백테스트", messageText="백테스트"),
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
    IMAGE_URL = "https://firebasestorage.googleapis.com/v0/b/linchfin-27c35.appspot.com/o/portfolio%2Fportfolio.png?alt=media&token=7408b757-6faf-439a-b413-9967e5e16e4d"

    def build_replies(self, payload) -> List[ABCSkillResponse]:
        _portfolio = get_items(key="portfolio")
        if _portfolio and "weights" in _portfolio:
            return [
                SimpleText(text=f"{_portfolio['base_date']} 기준 포트폴리오입니다."),
                ItemCard(
                    thumbnail=self.get_thumbnail(),
                    itemList=[
                        ItemListRow(title=k, description=f"{round(float(v) * 100, 3)}%")
                        for k, v in sorted(
                            _portfolio["weights"].items(),
                            key=lambda _w: _w[1],
                            reverse=True,
                        )
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


class BacktestBot(MetaBot):
    ACTION_KEYWORDS = ["백테스트"]

    IMAGE_URL = "https://linchfin-kakaoi.herokuapp.com/api/v1/backtest/result"

    def build_replies(self, payload) -> List[ABCSkillResponse]:
        return [
            ItemCard(
                thumbnail=self.get_thumbnail(),
                itemList=[ItemListRow(title="AA", description="BBB")],
                buttons=[MessageButton(label="포트폴리오", messageText="포트폴리오")],
            )
        ]

    def get_thumbnail(self) -> Thumbnail:
        return Thumbnail(
            imageUrl=self.IMAGE_URL, width=800, height=800, fixedRatio=False
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
