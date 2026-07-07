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
    NTEGAME = "ntegame"


CODE_URLS: Final[dict[str, dict[CodeSource, str]]] = {
    Game.wuwa: {
        CodeSource.GAMESRADAR: "https://www.gamesradar.com/games/rpg/wuthering-waves-codes-redeem/",
        CodeSource.WUTHERINGGG: "https://wuthering.gg/codes",
        CodeSource.PCGAMESN: "https://www.pcgamesn.com/wuthering-waves/codes",
    },
    Game.nte: {
        CodeSource.NTEGAME: "https://www.ntegame.com/codes/",
    },
    Game.endfield: {
        CodeSource.GAMESRADAR: "https://www.gamesradar.com/games/rpg/arknights-endfield-codes/",
        CodeSource.GAME8: "https://game8.co/games/Arknights-Endfield/archives/571509",
    },
}
