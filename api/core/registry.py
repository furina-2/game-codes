from __future__ import annotations

from api.constants import Game

from api.core.base import GameIntegration
from api.games.bluearchive import BlueArchiveIntegration
from api.games.endfield import EndfieldIntegration
from api.games.nte import NTEIntegration
from api.games.wuwa import WuWaIntegration

_registry: dict[str, GameIntegration] = {}


def register(game: str, integration: GameIntegration) -> None:
    _registry[game] = integration


def get_integration(game: str) -> GameIntegration | None:
    return _registry.get(game)


def list_games() -> list[str]:
    return list(_registry.keys())


register(Game.wuwa, WuWaIntegration())
register(Game.nte, NTEIntegration())
register(Game.bluearchive, BlueArchiveIntegration())
register(Game.endfield, EndfieldIntegration())
