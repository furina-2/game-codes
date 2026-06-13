from __future__ import annotations

import httpx
from loguru import logger
from api.constants import CodeStatus, Game

from api.core.base import GameIntegration
from api.utils import load_uids


class ArknightsIntegration(GameIntegration):
    game = Game.arknights
    has_web_redemption = True

    async def get_auth(self) -> dict:
        uids = load_uids()
        return {"uid": uids.get("arknights", "")}

    async def verify_code(self, code: str) -> CodeStatus:
        auth = await self.get_auth()
        uid = auth.get("uid", "")
        if not uid:
            logger.warning("No UID for Arknights verification")
            return CodeStatus.UNVERIFIED
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                resp = await client.post(
                    "https://arknights.global/gift/api/redeem",
                    data={"uid": uid, "code": code},
                )
                if resp.status_code == 200:
                    return CodeStatus.OK
                return CodeStatus.NOT_OK
            except Exception as e:
                logger.error(f"Arknights verification failed: {e}")
                return CodeStatus.UNVERIFIED
