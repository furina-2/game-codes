from __future__ import annotations

from abc import ABC, abstractmethod

from api.constants import CodeStatus, Game

from api.codes.parsers import ParserFunc
from api.codes.sources import CODE_URLS, CodeSource


class GameIntegration(ABC):
    game: str
    has_web_redemption: bool = False

    @property
    def code_urls(self) -> dict[CodeSource, str]:
        return CODE_URLS.get(self.game, {})

    @property
    def parsers(self) -> dict[CodeSource, ParserFunc]:
        return {}

    @abstractmethod
    async def verify_code(self, code: str) -> CodeStatus:
        ...

    async def get_auth(self) -> dict:
        return {}

    async def check_code(self, code: str) -> CodeStatus:
        if not self.has_web_redemption:
            return CodeStatus.OK
        return await self.verify_code(code)
