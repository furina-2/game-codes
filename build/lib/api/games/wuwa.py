from __future__ import annotations

from api.constants import CodeStatus, Game

from api.core.base import GameIntegration


class WuWaIntegration(GameIntegration):
    game = Game.wuwa
    has_web_redemption = False

    async def verify_code(self, code: str) -> CodeStatus:
        return CodeStatus.UNVERIFIED

    async def get_auth(self) -> dict:
        return {}
