from __future__ import annotations

from enum import StrEnum
from typing import Final

from api.constants import Game


class CodeSource(StrEnum):
    GAMESRADAR = "gamesradar"
    GAME8 = "game8"
    GAMEWITH = "gamewith"
    PCGAMESN = "pcgamesn"
    VG247 = "vg247"
    WUTHERINGGG = "wutheringgg"


CODE_URLS: Final[dict[str, dict[CodeSource, str]]] = {
    Game.wuwa: {},
    Game.nte: {},
    Game.endfield: {},
}
