from __future__ import annotations

import json
from pathlib import Path

from api.constants import Game

COOKIES_PATH = Path("cookies.json")
UIDS_PATH = Path("uids.json")


def load_cookies() -> dict[str, str]:
    if COOKIES_PATH.exists():
        return json.loads(COOKIES_PATH.read_text())
    return {}


def load_uids() -> dict[str, str]:
    if UIDS_PATH.exists():
        return json.loads(UIDS_PATH.read_text())
    return {}


REDEEM_URLS: dict[str, str] = {
    Game.wuwa: "",
    Game.nte: "",
    Game.bluearchive: "https://mcoupon.nexon.com/bluearchive",
    Game.arknights: "https://arknights.global/gift",
    Game.endfield: "",
}
