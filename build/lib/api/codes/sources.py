from __future__ import annotations

from enum import StrEnum
from typing import Final

from api.constants import Game


class CodeSource(StrEnum):
    GAMESRADAR = "gamesradar"
    GAMERANT = "gamerant"
    GAME8 = "game8"
    GAMEWITH = "gamewith"
    DEXERTO = "dexerto"


CODE_URLS: Final[dict[str, dict[CodeSource, str]]] = {
    Game.wuwa: {
        CodeSource.GAMESRADAR: "https://www.gamesradar.com/games/rpg/wuthering-waves-codes-redeem/",
        CodeSource.GAMERANT: "https://gamerant.com/wuthering-waves-codes/",
    },
    Game.nte: {
        CodeSource.GAMESRADAR: "https://www.gamesradar.com/games/action-rpg/neverness-to-everness-codes-nte/",
        CodeSource.GAME8: "https://game8.co/games/Neverness-to-Everness/archives/593718",
        CodeSource.GAMEWITH: "https://gamewith.net/nte/74145",
    },
    Game.bluearchive: {
        CodeSource.GAMERANT: "https://gamerant.com/blue-archive-codes/",
        CodeSource.DEXERTO: "https://www.dexerto.com/codes/blue-archive-codes-3311458/",
    },
    Game.arknights: {
        CodeSource.GAMEWITH: "https://gamewith.net/arknights/article/18979",
    },
    Game.endfield: {
        CodeSource.GAMESRADAR: "https://www.gamesradar.com/games/rpg/arknights-endfield-codes/",
        CodeSource.GAME8: "https://game8.co/games/Arknights-Endfield/archives/571509",
    },
}
