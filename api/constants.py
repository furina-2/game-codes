from __future__ import annotations

from typing import Final


class Game:
    wuwa: Final[str] = "wuwa"
    nte: Final[str] = "nte"
    bluearchive: Final[str] = "bluearchive"
    endfield: Final[str] = "endfield"

    @classmethod
    def values(cls) -> list[str]:
        return [v for k, v in vars(cls).items() if isinstance(v, str) and not k.startswith("_")]


class CodeStatus:
    OK: Final[str] = "OK"
    NOT_OK: Final[str] = "NOT_OK"
    UNVERIFIED: Final[str] = "UNVERIFIED"
