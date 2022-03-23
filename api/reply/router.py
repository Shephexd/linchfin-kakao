from typing import List, Type
from api.kakaoi.request import SkillPayload
from api.kakaoi.response.skills import (
    ABCSkillResponse,
    SkillResponse,
    SimpleText,
    QuickReply,
)
from api.reply.bots import MetaBot, PortfolioBot, UniverseBot


class BotRouter:
    bot_map = {PortfolioBot: [], UniverseBot: []}

    def reply(self, payload: SkillPayload) -> SkillResponse:
        _bot = self.select(payload=payload)
        return _bot.reply(payload=payload)

    def select(self, payload: SkillPayload) -> MetaBot:
        for _bot_class, _ in self.bot_map.items():
            matched_bot_class = _bot_class.match(payload.input_text)
            if matched_bot_class and issubclass(matched_bot_class, MetaBot):
                return matched_bot_class()
        return MetaBot()
