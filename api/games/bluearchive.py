from __future__ import annotations

import httpx
from loguru import logger
from api.constants import CodeStatus, Game

from api.core.base import GameIntegration
from api.utils import load_cookies, load_uids


class BlueArchiveIntegration(GameIntegration):
    game = Game.bluearchive
    has_web_redemption = True

    async def get_auth(self) -> dict:
        cookies = load_cookies()
        uids = load_uids()
        return {
            "cookie": cookies.get("bluearchive", ""),
            "member_code": uids.get("bluearchive", ""),
        }

    async def verify_code(self, code: str) -> CodeStatus:
        auth = await self.get_auth()
        member_code = auth.get("member_code", "")
        if not member_code:
            logger.warning("No member code for Blue Archive verification")
            return CodeStatus.UNVERIFIED
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                resp = await client.post(
                    "https://mcoupon.nexon.com/bluearchive/api/use",
                    data={
                        "memberCode": member_code,
                        "couponCode": code,
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
                if resp.status_code == 200:
                    return CodeStatus.OK
                return CodeStatus.NOT_OK
            except Exception as e:
                logger.error(f"Blue Archive verification failed: {e}")
                return CodeStatus.UNVERIFIED
