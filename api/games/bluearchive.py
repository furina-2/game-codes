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
        """Check code validity via Nexon's coupon API.
        
        Returns:
            OK if the API confirms the code is valid and redeemable.
            UNVERIFIED if the API returns code 95130 (already used or expired).
            NOT_OK if the API returns any other error (invalid code, etc.).
        """
        auth = await self.get_auth()
        member_code = auth.get("member_code", "")
        cookie = auth.get("cookie", "")
        if not member_code or not cookie:
            logger.warning("No member code or cookie for Blue Archive verification")
            return CodeStatus.UNVERIFIED
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                resp = await client.post(
                    "https://mcoupon.nexon.com/bluearchive/coupon/api/v1/characters-by-npacode",
                    json={
                        "npaCode": member_code,
                        "coupon": code,
                        "region": "asia",
                    },
                    headers={
                        "Content-Type": "application/json",
                        "Cookie": cookie,
                        "User-Agent": "Mozilla/5.0",
                        "Referer": "https://mcoupon.nexon.com/bluearchive",
                    },
                )
                data = resp.json()
                api_code = data.get("code")
                result = data.get("result", False)
                if result:
                    return CodeStatus.OK
                if api_code == 95130:
                    return CodeStatus.UNVERIFIED
                return CodeStatus.NOT_OK
            except Exception as e:
                logger.error(f"Blue Archive verification failed: {e}")
                return CodeStatus.UNVERIFIED
